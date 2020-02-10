import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import random
import requests
from bs4 import BeautifulSoup


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("library/creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("parsed").sheet1  # Open the spreadhseet

data = sheet.get_all_records()  # Get a list of all records
all_ids = [x['id'] for x in data]

p = requests.get("http://crocus-expo.ru/exhibition/plan.php")
soup = BeautifulSoup(p.text, 'html.parser')

all_blocks = soup.find(class_='ac-container')
all_divs = all_blocks.find_all('div' )

#Parse all events on page
for val in all_divs: 
    try:
        #Here we get name and option blocks
        data1 = val.find_all('label', attrs={'class': 'bgs'}) 
        data2 = val.find_all('article', attrs={'class': 'ac-full'})
        
        go = lambda a, b : True if (len(a) > 0 and len(b) > 0) else False
        answer = go(data1, data2)
        if(answer):
            mezh = []
            id = val.find('label', attrs={'class': 'bgs'}).get('for')
            name = data1[0].find('img', attrs={'class': 'leftimg'}).get('alt')
            category = data1[0].find('em').text
            data = data1[0].find('b').text
            dop_info = data2[0].find_all('div', attrs={'class': 'col-md-6 col-sm-6 co'})
            dop_info = dop_info[1].find('p')
            url = dop_info.find('a').get('href')
            mezh = [id, name, category, data, url]
            if id not in all_ids:
                if(len(str(mezh[0])) > 0):
                    sheet.insert_row(mezh, 2)
    except:
        pass
