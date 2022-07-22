'''Testing
'''
import os
import pandas as pd
import requests
import datetime
import xml.etree.ElementTree as ET

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import settings


def get_credentials():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', settings.SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', settings.SCOPES)
            creds = flow.run_local_server(port=58436, redirect_uri_trailing_slash=True)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_data(creds: Credentials = get_credentials()) -> pd.DataFrame:
    try:
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=settings.SPREADSHEET_ID,
                                    range=settings.RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('no data found')
            return

        print('data:')
        #print(values)
        df_data = pd.DataFrame(values[0:], columns=['nn', 'order_id', 'usd_value', 'delivery_date'])
        df_data['usd_value'] = df_data['usd_value'].astype(float)
        
        usd_to_rub_rate = get_exchange_rate()
        
        df_data['rub_value'] = df_data['usd_value'] * usd_to_rub_rate
        print(df_data)
        # for row in values:
        #     print(f'{row[0]} {row[1]} {row[2]} {row[3]}')
    except HttpError as err:
        print(f'error: {err}')
        return
    
def get_exchange_rate() -> float:
    today = datetime.datetime.now(tz=datetime.timezone.utc).strftime('%d/%m/%Y')
    url = f'https://www.cbr.ru/scripts/XML_daily.asp'
    
    r = requests.get(url)
    if r.status_code != 200:
        print(f'error: {r.status_code}')
        return
    root = ET.fromstring(r.content)
    
    for child in root.iter('Valute'):
        if child.find('CharCode').text == 'USD':
            usd_rate = child.find('Value').text
            return float(usd_rate.replace(',', '.'))
        
    
get_data(creds = get_credentials())

