'''
Setup and Base Functions for all analytics
'''
import json
import urllib.request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Set up Google Sheets connection
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
if os.path.isfile('client_secret.json'):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
else:
    creds = {}
    creds["type"] = "service_account"
    creds["project_id"] = os.getenv('PROJECT_ID')
    creds["private_key_id"] = os.getenv('PRIVATE_KEY_ID')
    creds["private_key"] = os.getenv('PRIVATE_KEY').replace("\\n", "\n")
    creds["client_email"] = os.getenv('CLIENT_EMAIL')
    creds["client_id"] = os.getenv('CLIENT_ID')
    creds["auth_uri"] = "https://accounts.google.com/o/oauth2/auth"
    creds["token_uri"] = "https://accounts.google.com/o/oauth2/token"
    creds["auth_provider_x509_cert_url"] = "https://www.googleapis.com/oauth2/v1/certs"
    creds["client_x509_cert_url"] = os.getenv('CLIENT_X509_CERT_URL')
    # print(json.dumps(creds,ident=2))
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)

gc = gspread.authorize(credentials)
wks = gc.open("HR.info Analytics")

def open_url(url):
    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req).read()
    content = json.loads(r.decode('utf-8'))
    return content