"""Settings file
"""
import os

SPREADSHEET_ID = '1ogdQQD10AM2cBwprYhm-Oh4oAeFzfaoQAgsfYCXwzkQ'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
RANGE_NAME = 'Data!A2:D'

DATABASE = 'postgresql://postgres:postgres@localhost:5432/canalservice'
GOOGLE_API_FOLDER = f'{os.getcwd()}/google_api'
GOOGLE_API_TOKEN_PATH = f'{GOOGLE_API_FOLDER}/token.json'
GOOGLE_API_CREDENTIALS_PATH = f'{GOOGLE_API_FOLDER}/credentials.json'
SQL_ECHO = False

CHECK_INTERVAL = 30 # in seconds

