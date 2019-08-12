import os
import pprint
import sys

from sparkpost import SparkPost
from sparkpost.exceptions import SparkPostAPIException

from secrets import SPARKPOST_API_KEY

def email_post(request):
    try:
        email_address = os.environ.get('EMAIL_ADDRESS')
        body = request.get_json()
        accountName = body['metadata']['accountName']
        if body['metadata']['type'] == 'balance':
            subject = 'Balance Notification for {}'.format(accountName)
        elif body['metadata']['type'] == 'transaction':
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
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return 'Error', 500
