"""Main module of the application
"""
import threading
from threading import Thread
from datetime import datetime
import pandas as pd
import settings
import bot
import google_sheet_worker as gsw

def main(interval: int = settings.CHECK_INTERVAL) -> None:
    bot_thread = Thread(target=bot.start_bot)
    threading.Timer(interval, main).start()
    
    google_creds = gsw.get_credentials(api_key_path=settings.GOOGLE_API_TOKEN_PATH,
                                       credentials_path=settings.GOOGLE_API_CREDENTIALS_PATH,
                                       scopes=settings.SCOPES)
    data = gsw.get_data(creds=google_creds)
    gsw.dump_data_to_sql(data)
    send_notification('test', data)
    print(f'data dumped to sql, time: {datetime.now()}')

# TODO: prettify the message layout
# TODO: notify only if new data added? (try through the settings file and compare with the last time)
def send_notification(message: str, data: pd.DataFrame) -> None:
    today = datetime.now()
    # expired_i = data.index[data['delivery_date'] < today].tolist()
    expired_data = data.loc[data['delivery_date'] < today]
    message = f"""
    Дата доставки устарела у позиций:
    {expired_data[['order_id', 'delivery_date']]
        .to_string(index=False)
        .replace('order_id', '№ заказа')
        .replace('delivery_date', 'дата доставки')
    }
    """.replace('\t', '')
    bot.notify_users(message)
    
    

if __name__ == '__main__':
    main()
