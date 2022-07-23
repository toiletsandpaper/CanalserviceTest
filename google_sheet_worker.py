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
import database


def get_credentials(api_key_path: str = settings.GOOGLE_API_TOKEN_PATH,
                        credentials_path: str = settings.GOOGLE_API_CREDENTIALS_PATH,
                        scopes: list[str]= settings.SCOPES) -> Credentials:
    creds = None
    if os.path.exists(api_key_path):
        creds = Credentials.from_authorized_user_file(api_key_path, scopes=scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes=scopes)
            creds = flow.run_local_server(port=58436, redirect_uri_trailing_slash=True)
        with open(api_key_path, 'w', encoding="UTF-8") as token:
            token.write(creds.to_json())
    return creds


# TODO: find how to get the "last modified date" of the spreadsheet 
# https://stackoverflow.com/questions/43411138/get-google-sheets-last-edit-date-using-sheets-api-v4-java
# https://developers.google.com/drive/api/v3/reference/files/get
# looks like we should use Drive API, but it can be only done if we have access to gdrive folder
def get_data(creds: Credentials = get_credentials()) -> pd.DataFrame:
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Pylint can not understand that we are using the correct service. All good to run.
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=settings.SPREADSHEET_ID,
                                    range=settings.RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('no data found')
            return

        print('data:')
        # print(values)
        df_data = pd.DataFrame(values[0:], columns=['nn', 'order_id', 'usd_value', 'delivery_date'])
        df_data['usd_value'] = df_data['usd_value'].astype(float)
        df_data['nn'] = df_data['nn'].astype(int)
        
        usd_to_rub_rate = get_exchange_rate()
        
        df_data['rub_value'] = df_data['usd_value'] * usd_to_rub_rate
        print(df_data.tail())
        return df_data
        # for row in values:
        #     print(f'{row[0]} {row[1]} {row[2]} {row[3]}')
    except HttpError as err:
        print(f'error: {err}')
        return


def dump_data_to_sql(df_data: pd.DataFrame):
    database.dump_to_sql(df_data)


def get_exchange_rate() -> float:
    # today = datetime.datetime.now(tz=datetime.timezone.utc).strftime('%d/%m/%Y')
    url = f'https://www.cbr.ru/scripts/XML_daily.asp'
    request = requests.get(url)
    if request.status_code != 200:
        print(f'error: {request.status_code}')
        return
    root = ET.fromstring(request.content)
    for child in root.iter('Valute'):
        if child.find('CharCode').text == 'USD':
            usd_rate = child.find('Value').text
            return float(usd_rate.replace(',', '.'))
