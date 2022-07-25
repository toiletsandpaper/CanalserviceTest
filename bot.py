import telebot
import os
import csv
import settings

token = os.environ['TELEGRAM_BOT_TOKEN']
bot = telebot.TeleBot(token)



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 
                    'Привет, я бот для работы с гугл таблицей по тестовому заданию от Canalservice')


@bot.message_handler(commands=['addusernotification', 'aun', 'add'])
def add_user_notification(message):
    bot.send_message(message.chat.id, add_to_notification_list(message.chat.id))


@bot.message_handler(commands=['removeusernotification', 'run', 'remove'])
def remove_user_notification(message):
    bot.send_message(message.chat.id, remove_from_notification_list(message.chat.id))


def add_to_notification_list(chat_id) -> str:
    list_of_users = None
    with open(settings.TELEGRAM_BOT_NOTIFICATION_LIST_PATH, 'r+', newline='') as f:
        list_of_users = csv.reader(f, delimiter=',').__next__()
        if str(chat_id) in list_of_users:
            return "Вы уже были добавлены в список рассылки"
        else:
            list_of_users.append(str(chat_id))
    with open(settings.TELEGRAM_BOT_NOTIFICATION_LIST_PATH, 'w+', newline='') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(list_of_users)
        return "Вы добавлены в список рассылки"


def remove_from_notification_list(chat_id) -> str:
    list_of_users = None
    with open(settings.TELEGRAM_BOT_NOTIFICATION_LIST_PATH, 'r+', newline='') as f:
        list_of_users = csv.reader(f, delimiter=',').__next__()
        if str(chat_id) in list_of_users:
            list_of_users.remove(str(chat_id))
        else:
            return 'Вас не было в списке рассылки'
    with open(settings.TELEGRAM_BOT_NOTIFICATION_LIST_PATH, 'w+', newline='') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(list_of_users)
    return 'Вы были удалены из списка рассылки'


def notify_users(message):
    with open(settings.TELEGRAM_BOT_NOTIFICATION_LIST_PATH, 'r+', newline='') as f:
        list_of_users = csv.reader(f, delimiter=',').__next__()
        for user in list_of_users:
            bot.send_message(user, message, parse_mode='Markdown')

def start_bot():
    """Creates '/bot_data/notification_list.csv' if it doesn't exist and starts bot
    """    
    if not os.path.exists(settings.TELEGRAM_BOT_NOTIFICATION_LIST_PATH):
        with open(settings.TELEGRAM_BOT_NOTIFICATION_LIST_PATH, 'w+', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow([])
    bot.infinity_polling()

def stop_bot():
    bot.stop_polling()
