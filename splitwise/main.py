import json
import os
import requests

from secrets import SPLITWISE_CONSUMER_KEY, SPLITWISE_CONSUMER_SECRET

TOKEN_URL = 'https://secure.splitwise.com/oauth/token'
API_BASE_URL = 'https://www.splitwise.com/api/v3.0/'

def get_access_token():
    query_params = {
        'grant_type': 'client_credentials',
        'client_id': SPLITWISE_CONSUMER_KEY,
        'client_secret': SPLITWISE_CONSUMER_SECRET,
    }
    resp = requests.get(TOKEN_URL, params=query_params)
    parsed = resp.json()
    if parsed['token_type'] != 'bearer':
        raise Exception('unknown token type: {}'.format(parsed['token_type']))

    return parsed['access_token']

def get_group(bearer_token):
    headers = {
        'Authorization': 'Bearer {}'.format(bearer_token),
    }
    resp = requests.get(API_BASE_URL + 'get_groups', headers=headers)
    group_name = os.getenv('SPLITWISE_GROUP_NAME')
    group = next(group for group in resp.json()['groups'] if group['name'] == group_name)
    return group

def get_current_user(bearer_token):
    headers = {
        'Authorization': 'Bearer {}'.format(bearer_token),
    }
    resp = requests.get(API_BASE_URL + 'get_current_user', headers=headers)
    return resp.json()

def post_charge(bearer_token, curr_user, group, name, amount):
    body = {
        'group_id': group['id'],
        'currency_code': 'USD',
        'cost': amount,
        'description': name,
    }

    headers = {
        'Authorization': 'Bearer {}'.format(bearer_token),
    }

    for idx, user in enumerate(group['members']):
        body['users__{}__user_id'.format(idx)] = user['id']

        # round to 2 decimal places, last person takes the remainder
        amt_owed = round(float(amount) / len(group['members']), 2)
        if idx != len(group['members']) - 1:
            owed_share = amt_owed
        else:
            owed_share = amount - (amt_owed * (len(group['members']) - 1))

        if user['id'] == curr_user['user']['id']:
            paid_share = amount
        else:
            paid_share = 0.

        body['users__{}__owed_share'.format(idx)] = owed_share
        body['users__{}__paid_share'.format(idx)] = paid_share

    resp = requests.post(API_BASE_URL + 'create_expense', headers=headers, data=body)
    parsed = resp.json()
    if len(parsed['errors']) > 0:
        raise Exception('charge request contains errors: {}'.format(resp.text))
    print(resp.text)

def handle_charge(request):
    body = request.get_json()

    name = body['item']['name']
    amount = body['item']['amount']
    bearer_token = get_access_token()
    group = get_group(bearer_token)
    curr_user = get_current_user(bearer_token)
    post_charge(bearer_token, curr_user, group, name, amount)
