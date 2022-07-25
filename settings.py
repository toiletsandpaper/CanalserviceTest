"""Settings file
"""
import os

SPREADSHEET_ID = '1ogdQQD10AM2cBwprYhm-Oh4oAeFzfaoQAgsfYCXwzkQ' # ID of the spreadsheet (found in the URL)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
RANGE_NAME = 'Data!A2:D'

DATABASE = 'postgresql+psycopg2://postgres:postgres@localhost:5432/canalservice'
GOOGLE_API_FOLDER = f'{os.getcwd()}/google_api'
GOOGLE_API_TOKEN_PATH = f'{GOOGLE_API_FOLDER}/token.json'
GOOGLE_API_CREDENTIALS_PATH = f'{GOOGLE_API_FOLDER}/credentials.json'
SQL_ECHO = False

CHECK_INTERVAL = 30 # in seconds #! MAKE SHURE THIS IS NOT SMALLER THAN NOTIFICATION_CHECK_INTERVAL

TELEGRAM_BOT_DATA_FOLDER = f'{os.getcwd()}/bot_data'
TELEGRAM_BOT_NOTIFICATION_LIST_PATH = f'{TELEGRAM_BOT_DATA_FOLDER}/notification_list.csv'

NOTIFICATION_TIME_H, NOTIFICATION_TIME_M, NOTIFICATION_TIME_S = (0, 0, 0) # in (H,M,S) format
NOTIFICATION_CHECK_INTERVAL = 20 # in seconds  #! MAKE SURE THIS IS SMALLER THAN CHECK_INTERVAL
