import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import json

def lambda_handler(event, context):
   r = requests.get('https://www.tempestlukeshospital.org/data/erwait?_format=json')
   wait_data = json.loads(r.text)

   # print(f"Wait Time: {wait_data['minutes']}, check Time: {wait_data['generated']}")

   # use creds to create a client to interact with the Google Drive API
   scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
   creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
   client = gspread.authorize(creds)

   # Find a workbook by name and open the first sheet
   # Make sure you use the right name here.
   worksheet = client.open_by_key('1JjXRidjRz-YiSVrdRqhkpvyCUi7X52TtIZvkBroVme0').worksheet("data")

   worksheet.append_row(["Tempe St. Lukes",wait_data['generated'], wait_data['minutes']])

if __name__ =='__main__':
   lambda_handler("", "")
