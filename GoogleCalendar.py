import datetime
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TOKEN = os.path.join(BASE_PATH, "token.json")
CREDNTIALS = os.path.join(BASE_PATH, "credentials.json")

EVENTS = list()

def main(maxResults):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDNTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=maxResults, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        # EVENTS.append(f"{start}, {event['summary']}")
        EVENTS.append({
            "summary": event['summary'],
            "startTime": datetime.datetime.fromisoformat(start).replace(tzinfo=None),
            "endTime": datetime.datetime.fromisoformat(end).replace(tzinfo=None)
        })




def clearEvents():
    EVENTS.clear()


def getHoursBetween(a, b):
    return abs((a - b) // 3600)


def getEvents():
    currentEvent = None
    nextEvent = None
    currentTime = datetime.datetime.now()
    
    if currentTime < EVENTS[0]['startTime']: 
        currentEvent = {
            "summary": "Nothing",
            "startTime": currentTime,
            "endTime": EVENTS[0]['startTime']
        }
        nextEvent = EVENTS[0]
    if (currentTime >= EVENTS[0]['startTime']) and (currentTime <= EVENTS[0]['endTime']): 
        currentEvent = EVENTS[0]
        nextEvent = EVENTS[1]
    return currentEvent, nextEvent

if __name__ == '__main__':
    main(10)
    [print("[*] ", f"{EVENTS[i]['summary']}\t", " "*15, f" {EVENTS[i]['startTime'].strftime('%I:%M %p')} - {EVENTS[i]['endTime'].strftime('%I:%M %p')}") for i in range(len(EVENTS))]
    # while True:
    #     try:
    #         main(2)
    #         print("")
    #         print("Current Task:", EVENTS[0])
    #         print("Next Task:", EVENTS[1])
    #         print("")

    #         EVENTS.clear()
    #         time.sleep(5)
    #     except Exception as e:
    #         print(e)

    #     except KeyboardInterrupt:
    #         print("Keyboard Interrupt")
    #         break

    #     finally:
    #         continue
