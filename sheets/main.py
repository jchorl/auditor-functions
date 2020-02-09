import csv
import io
import json
import os.path
import pickle

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

FINANCE_SPREADSHEET_ID = os.getenv("FINANCE_SPREADSHEET_ID")
TEMPLATE_SHEET_ID = os.getenv("TEMPLATE_SHEET_ID")


def get_google_creds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        # cloud functions have a read-only fs so just refresh the token every time
        # with open('token.pickle', 'wb') as token:
        #     pickle.dump(creds, token)

    return creds


def sheet_exists(service, name):
    try:
        service.spreadsheets().get(
                spreadsheetId=FINANCE_SPREADSHEET_ID,
                ranges=[name],
        ).execute()
        return True
    except HttpError as e:
        parsed = json.loads(e.content)
        if parsed['error']['status'] != 'INVALID_ARGUMENT':
            raise
    return False


def create_sheet(service, name):
    new_sheet = service.spreadsheets().sheets().copyTo(
            spreadsheetId=FINANCE_SPREADSHEET_ID,
            sheetId=TEMPLATE_SHEET_ID,
            body={
                "destinationSpreadsheetId": FINANCE_SPREADSHEET_ID,
            },
    ).execute()
    new_sheet_id = new_sheet['sheetId']
    service.spreadsheets().batchUpdate(
            spreadsheetId=FINANCE_SPREADSHEET_ID,
            body={
                "requests": [{
                    "updateSheetProperties": {
                        "fields": "title",
                        "properties": {
                            "sheetId": new_sheet_id,
                            "title": name,
                        },
                    }
                }],
            },
    ).execute()


def add_transaction_to_sheet(service, account, date, name, amount, categories):
    # convert categories to csv
    categories_buffer = io.StringIO()
    categories_writer = csv.writer(categories_buffer)
    categories_writer.writerow(categories)
    categories_str = categories_buffer.getvalue().rstrip()

    values = [
        date,
        name,
        amount,  # real amount
        categories_str,  # real categories
        amount,  # effective amount
        categories[-1] if len(categories) > 0 else '',  # effective category
        'No',  # ack
    ]

    body = {
        'values': [values],
    }

    service.spreadsheets().values().append(
        spreadsheetId=FINANCE_SPREADSHEET_ID, range=account,
        valueInputOption='USER_ENTERED', body=body).execute()


def process_transaction(request):
    body = request.get_json()
    account = body['item']['accountName']
    date = body['item']['date']
    name = body['item']['name']
    amount = body['item']['amount']
    categories = body['item']['category']

    creds = get_google_creds()
    service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
    if not sheet_exists(service, account):
        create_sheet(service, account)
    add_transaction_to_sheet(service, account, date, name, amount, categories)
