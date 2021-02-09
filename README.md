# gmail-get-attached
Python code to get all attachment from email based on search criteria  

## Prerequisite
1. Python
2. Gmail account

## Preparation
- Enable G-Mail API and G-Drive API in your google console  
  gmail : [https://developers.google.com/gmail/api/quickstart/python]  
  gdrive : [https://developers.google.com/drive/api/v3/quickstart/python]
- Copy "credential.json" from Google Console to location of python code
- Install require package
  ```
  google-api-python-client  
  google-auth-httplib2  
  google-auth-oauthlib
  ```
- Run the code with
  ```
  GetMailAtt.GetMail('Search Criteria','Destination Folder')
  ```
  Search Criteria = Criteria to search for specific mail in your mail box (same as search text you type in your g-mail search box)  
  Destination Folder = Folder to download all attached document (reference from code folder)
