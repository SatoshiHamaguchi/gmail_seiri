import os, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)

    return creds

def get_emails():
    service = build('gmail', 'v1', credentials=authenticate())

    results = service.users().messages().list(
        userId='me',
        maxResults=5,
        q='is:unread'
    ).execute()

    messages = results.get('messages', [])

    for msg in messages:
        detail = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['Subject', 'From']
        ).execute()

        headers = {h['name']: h['value'] for h in detail['payload']['headers']}
        print(f"From   : {headers.get('From')}")
        print(f"Subject: {headers.get('Subject')}")
        print("─" * 40)

get_emails()