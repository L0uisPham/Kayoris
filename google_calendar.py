
import pytz
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils import parse_event

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def search_events(creds):
    service = build("calendar", "v3", credentials=creds)

    # Set the time range for today
        # Get the current time in UTC
    utc_time = datetime.datetime.utcnow()
    utc_time = datetime.datetime.utcnow()

    # Define the Eastern Timezone
    eastern = pytz.timezone('US/Eastern')

    # Convert UTC time to Eastern Time
    now = utc_time.replace(tzinfo=pytz.utc).astimezone(eastern)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    now = now.isoformat() 
    time_min = start_of_day.isoformat()   # Start of the current day in UTC
    time_max = end_of_day.isoformat()     # End of the current day in UTC
    
    print("Getting all events for the current day")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    if not events:
        print("No events found for today.")
        return

    starts=[]
    ends=[]
    list_events=[]
    # Prints the start and name of each event
    for event in events:
        starts.append(event['start'].get('dateTime', event['start'].get('date')))
        ends.append(event['end'].get('dateTime', event['end'].get('date')))
        list_events.append(event['summary'])
    
    return starts, ends, list_events


def create_event(query ,creds):
    service = build("calendar", "v3", credentials=creds)
    event_name, location, description, start_time, end_time = parse_event(query)
    event = {
        "summary": event_name,
        "location": location,
        "description": description,
        "colorId": 6,
        "start":{
            "dateTime": start_time,
            "timeZone": "America/New_York"
        },
        "end":{
            "dateTime": end_time,
            "timeZone": "America/New_York"
        }
    }
    event = service.events().insert(calendarId='primary', body=event).execute()


def today_events(query=''):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    
    try:
        if query == 'search':
            search_events(creds)
        else:
            create_event(query, creds)

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    today_events()