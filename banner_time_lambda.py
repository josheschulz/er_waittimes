import requests
import json
import lxml.html
import datetime
from datetime import timedelta
from io import StringIO
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def lambda_handler(event, context):
   r = requests.post('https://urgentcare.bannerhealth.com/Locations/Search', data={'searchString' : 85283, 'pageNumber' :1 ,'pageSize' :20, 'haveRooftopAccuracyForUserLocation' : 'False'})

   html = r.text
   parsed_html = lxml.html.parse(StringIO(r.text))
   
   root = parsed_html.getroot()

   locations = root.xpath('//div[@class="uc-card-list"][@data-isopen="True"]')

   # use creds to create a client to interact with the Google Drive API
   scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
   creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
   client = gspread.authorize(creds)

   # Find a workbook by name and open the first sheet
   # Make sure you use the right name here.
   worksheet = client.open_by_key('1JjXRidjRz-YiSVrdRqhkpvyCUi7X52TtIZvkBroVme0').worksheet("data")

   for div in locations:
      next_open = div.attrib['data-nexttimeavailableutc']
      id = div.attrib['id']

      current = datetime.datetime.utcnow()
      delta = datetime.datetime.strptime(next_open, '%Y-%m-%dT%H:%M:%S') - current
      minutes, seconds = divmod(delta.seconds, 60)
      # print(f"ID: {id}, Delta: {minutes}, Next: {div.attrib['data-nexttimeavailable']}, NextUTC: {next_open}, current: {current}")


      print(f"Wait Time: {minutes}, check Time: {current}, id: {id}")
      worksheet.append_row([id,current.strftime('%Y-%m-%dT%H:%M:%S' ),minutes])

if __name__ =='__main__':
   lambda_handler("", "")

#curl 'https://urgentcare.bannerhealth.com/Locations/Search' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:73.0) Gecko/20100101 Firefox/73.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'XSRF-TOKEN: undefined' -H 'X-Requested-With: XMLHttpRequest' -H 'Origin: https://urgentcare.bannerhealth.com' -H 'DNT: 1' -H 'Connection: keep-alive' \
#-H 'Referer: https://urgentcare.bannerhealth.com/' \
#-H 'Pragma: no-cache' -H 'Cache-Control: no-cache' --data 'searchString=85283&pageNumber=1&pageSize=20&haveRooftopAccuracyForUserLocation=False' 
