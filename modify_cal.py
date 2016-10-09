
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime as dt
import pytz

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

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
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_service_object():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    return service

def get_praku_cal(service_obj):

    praku_cal = service_obj.calendars().get(calendarId='primary').execute()

    return praku_cal['id']
    #updated_praku_cal = service.calendars().update(calendarId=praku_cal['id'], body=praku_cal).execute()



def create_event(calID, service_obj):
   
    startdate = dt.datetime(2016, 10, 8, 19, 45)

    enddate = dt.datetime(2016, 10, 8, 22)

    
    
    event = { 
            'summary' : 'Created via Python',
            'location' : '750 Farm Road',
            'description' : 'Created using Google Calendar APIs',
            
   
            'start' : {
                'dateTime' : startdate.isoformat(),
                'timeZone' : 'America/New_York',
                },
            'end' : {
                'dateTime' :  enddate.isoformat(),
                'timeZone' : 'America/New_York',
                },
            
            }
        

    event = service_obj.events().insert(calendarId=calID, body=event).execute()
    return event['id']

def get_today_events(calID, service_obj):
    today_date = dt.date.today().day
    today_month = dt.date.today().month
    today_year = dt.date.today().year

    end_of_day = dt.datetime(today_year, today_month, today_date, 23, 59, 59)
    local = pytz.timezone("America/New_York")
    local_dt = local.localize(end_of_day, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    print (utc_dt.isoformat())
    print (dt.datetime.utcnow().isoformat())

    eventList = service_obj.events().list(calendarId = calID, timeMin = dt.datetime.utcnow().isoformat() + 'Z', timeMax = end_of_day.isoformat() + '-04:00').execute()
    return eventList['items']

def remove_event(calID, eventID, service_obj):
    event_to_delete =  service_obj.events().get(calendarId = calID, eventId = eventID).execute()
    print ('Removing Event: ', event_to_delete['summary'])

    service_obj.events().delete(calendarId=calID, eventId = eventID).execute()
    

def main():
    service_obj = get_service_object()
    prakuCalID = get_praku_cal(service_obj)
    #eventID = create_event(prakuCalID, service_obj)
    today_events = get_today_events(prakuCalID, service_obj)
    for event in today_events:
        if 'Created via Python' in event['summary']:
            remove_event(prakuCalID, event['id'], service_obj)


    
if __name__ == '__main__':
    main()


