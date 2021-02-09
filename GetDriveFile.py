# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 14:43:22 2021

@author: methee.s
"""

from __future__ import print_function
import pickle, os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import io, shutil
SCOPES = ['https://www.googleapis.com/auth/drive']

def gfileGET(fileid, thepath):
    creds = None
    if os.path.exists('drive-token.pickle'):
        with open('drive-token.pickle', 'rb') as (token):
            creds = pickle.load(token)
    else:
        if creds and creds.valid or creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('drive-credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
    service = build('drive', 'v3', credentials=creds)
    request_info = service.files().get(fileId=fileid).execute()
    request = service.files().get_media(fileId=fileid)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    else:
        fh.seek(0)
        path = os.path.join(thepath, request_info['name'])
        with open(path, 'wb') as f:
            shutil.copyfileobj(fh, f, length=131072)
            f.close()
        print(request_info['name'] + ' -saved')
        return request_info['name']