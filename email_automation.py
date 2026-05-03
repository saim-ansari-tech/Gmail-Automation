import base64
import os
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail','v1',credentials=creds)

def get_emails_body(payload):
    
    body = ""
    if 'data' in payload.get('body',{}):
        raw = payload['body']['data']
        body = base64.urlsafe_b64decode(raw).decode('utf-8')

    elif 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                raw = part['body']['data']
                body = base64.urlsafe_b64decode(raw).decode('utf-8')
                break
    return body


def clean_body(raw_body):
    if not raw_body:
        return ""
    soup = BeautifulSoup(raw_body, 'html.parser')
    clean_text = soup.get_text(separator=' ', strip=True)
    return clean_text

def get_emails(max_results=5):
    service = get_gmail_service()
    results = service.users().messages().list(userId = 'me', maxResults = max_results,labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    
    emails = []
    for msg in messages:
        txt = service.users().messages().get(userId = 'me', id = msg['id']).execute()
        payload = txt['payload']
        headers = payload['headers']

        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'From':
                sender = header['value']

        body = clean_body(get_emails_body(payload))

        emails.append({
            'subject' : subject,
            'sender' : sender,
            'body' : body
        })

    return emails
    