"""Main module of the application
"""
import threading
from threading import Thread
import datetime
from django.conf import Settings
import pandas as pd
from tomlkit import date
import settings
import bot
import google_sheet_worker as gsw

def main(interval: int = settings.CHECK_INTERVAL) -> None:
    """Main function of the application

    Args:
        interval (int, optional): GoogleSheet check interval. Defaults to settings.CHECK_INTERVAL.
    """    
    bot_thread = Thread(target=bot.start_bot)
    threading.Timer(interval, main).start()
    
    google_creds = gsw.get_credentials(api_key_path=settings.GOOGLE_API_TOKEN_PATH,
                                       credentials_path=settings.GOOGLE_API_CREDENTIALS_PATH,
                                       scopes=settings.SCOPES)
    data = gsw.get_data(creds=google_creds)
    gsw.dump_data_to_sql(data)
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    if((today - datetime.timedelta(seconds=settings.NOTIFICATION_CHECK_INTERVAL)).day == yesterday.day):
    #if(datetime.datetime.now() + datetime.timedelta(seconds=settings.NOTIFICATION_CHECK_INTERVAL) > tomorrow_check_date):
        send_notification('', data)
    #send_notification('test', data)
    print(f'data dumped to sql, time: {datetime.datetime.now()}')

# TODO: notify only if new data added? (try through the settings file and compare with the last time)
def send_notification(message: str, data: pd.DataFrame) -> None:
    """Checks for expired and today delivery dates and sends notification to the user

    Args:
        message (str): additional message, placed on top of the notification
        data (pd.DataFrame): dataframe with data from the spreadsheet
    """    
    today = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    # expired_i = data.index[data['delivery_date'] < today].tolist()
    today_data = data.loc[lambda data: data['delivery_date'] == today]
    expired_data = data.loc[lambda data: data['delivery_date'] == today - datetime.timedelta(days=1)]

    print('today:', today)
    print('yesterday:', today - datetime.timedelta(days=1))
    if not today_data.empty:
        today_message = ("Сегодня дата доставки следующих заказов:\n" +
        f"``` {today_data[[ 'order_id', 'delivery_date']].to_string(index=False)}```")
    else:
        today_message = 'Сегодня нет заказов для доставки'

    if not expired_data.empty:
        expired_message = ("Заказы, которые должны были быть доставлены вчера:\n" +
        f"``` {expired_data[[ 'order_id', 'delivery_date']].to_string(index=False)}```")
    else:
        expired_message = "Заказов для доставки вчера не было"

    if message != '':
        message = f'{message}\n'
    message = f"""{message}{today_message}\n\n{expired_message}"""
    message = message.replace('order_id', '№ заказа |').replace('delivery_date', 'дата доставки')
    print(message)
    bot.notify_users(message)


if __name__ == '__main__':
    main()
