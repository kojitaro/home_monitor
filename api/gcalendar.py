from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import iso8601

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


class GCalendarEvent():
    def __init__(self, event):
        self.event = event

        self.summary = event['summary']

        if 'date' in self.event['start']:
            self.is_full_day = True
            dt = iso8601.parse_date(self.event['start']['date'])
        else:
            self.is_full_day = False
            dt = iso8601.parse_date(self.event['start']['dateTime'])

        self.startDate = datetime.date(dt.year, dt.month, dt.day)
        self.startTime = datetime.time(dt.hour, dt.minute, dt.second)

    def start_time_label(self):
        if self.is_full_day:
            return ""

        return "%02d:%02d" %(self.startTime.hour, self.startTime.minute)

    def start_date_label(self):
        return "%d日" %(self.startDate.day)


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_calendar_events(calendarId='primary', maxResults=10):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    eventsResult = service.events().list(
        calendarId=calendarId, timeMin=now, maxResults=maxResults, singleEvents=True,
        orderBy='startTime').execute()
    es = eventsResult.get('items', [])

    events = []
    for e in es:
        events.append(GCalendarEvent(e))

    return events


def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """

    print('Getting the upcoming 10 events')
    events = get_calendar_events()

    print(events)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
