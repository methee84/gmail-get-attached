# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from __future__ import print_function
import pickle, os.path, os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from GetDriveFile import gfileGET

def GetMail(search_criteria,download_folder):
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    if os.path.exists('mail-token.pickle'):
        with open('mail-token.pickle', 'rb') as (token):
            creds = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('mail-credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('mail-token.pickle', 'wb') as (token):
                pickle.dump(creds, token)   
    if creds:
        if not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('mail-credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('mail-token.pickle', 'wb') as (token):
                pickle.dump(creds, token)
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', q=(search_criteria)).execute()
        msglist = results.get('messages', [])
        msglist or print('No mail found.')
        for msgid in msglist:
            msg = service.users().messages().get(userId='me', id=(msgid['id'])).execute()
            for part in msg['payload']['parts']:
                if part['filename'] != '':
                    att = service.users().messages().attachments().get(userId='me', messageId=(msgid['id']), id=(part['body']['attachmentId'])).execute()
                    data = att['data']
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    path = os.path.join(download_folder, part['filename'])
                    with open(path, 'wb') as f:
                        f.write(file_data)
                        f.close()
                    print(part['filename'] + ' -saved')
                if part['mimeType'] == 'multipart/alternative':
                    for sub_part in part['parts']:
                        if sub_part['mimeType'] == 'text/html':
                            temp_data = sub_part['body']['data']
                            temp_data = base64.urlsafe_b64decode(temp_data.encode('UTF-8')).decode('utf-8')
                            fileid = temp_data.split('drive.google.com/file/d/')[1]
                            fileid = fileid.split('/view?')[0]
                            gfileGET(fileid, download_folder)     
        print('Download Completed')
    else:
        print('Credential Wrong!')