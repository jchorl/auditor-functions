import os
import pprint
import sys
import traceback

from sparkpost import SparkPost
from sparkpost.exceptions import SparkPostAPIException

from secrets import SPARKPOST_API_KEY

def email_post(request):
    try:
        email_address = os.environ.get('EMAIL_ADDRESS')
        body = request.get_json()
        if body['metadata']['type'] == 'balance':
            accountName = body['account']['name']
            subject = 'Balance Notification for {}'.format(accountName)
        elif body['metadata']['type'] == 'transaction':
            accountName = body['item']['accountName']
            subject = 'Transaction Notification for {}'.format(accountName)
        email_text = pprint.pformat(body)
        sp = SparkPost(SPARKPOST_API_KEY)
        try:
            sp.transmissions.send(
                recipients=[email_address],
                text=email_text,
                from_email='Auditor <notifications@auditor.joshchorlton.com>',
                subject=subject,
                track_opens=False,
                track_clicks=False,
            )
        except SparkPostAPIException as err:
            print("Error sending email through sparkpost. Got status {} and errors {}".format(err.status, err.errors))
            raise
    except Exception:
        traceback.print_exc()
        return 'Error', 500
