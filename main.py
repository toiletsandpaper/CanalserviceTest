"""Main module of the application
"""
import threading
import datetime
import settings
import google_sheet_worker as gsw

def main(interval: int = settings.CHECK_INTERVAL) -> None:
    threading.Timer(interval, main).start()
    google_creds = gsw.get_credentials(api_key_path=settings.GOOGLE_API_TOKEN_PATH,
                                       credentials_path=settings.GOOGLE_API_CREDENTIALS_PATH,
                                       scopes=settings.SCOPES)
    data = gsw.get_data(creds=google_creds)
    gsw.dump_data_to_sql(data)
    print(f'data dumped to sql, time: {datetime.datetime.now()}')

if __name__ == '__main__':
    main()