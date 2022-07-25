# Инструкция по запуску

## Шаг 1 - подготовка окружения

1. Напишите `@BotFather` в Telegram, создайте бота и сохраните токен куда-нибудь.
2. Откройте терминал и пропишите 
```bash
git clone https://github.com/toiletsandpaper/CanalserviceTest
```

3. Создайте окружение 
```bash
python -m venv venv
```
4. Зайдите в файл `/venv/bin/activate` и пропишите в конце файла:
```sh
deactivate () {
    unset TELEGRAM_BOT_TOKEN
}
export TELEGRAM_BOT_TOKEN="token"
```
5. Запустите окружение через терминал 
```bash
source /venv/bin/activate
```
6. Установите нужные библиотеки 
```bash
pip install -r requirements.txt
```

## Шаг 2 - подготовка GoogleSheet API

1. Просто используйте этот туториал по получению `credentials`
2. После того, как вы получите файл, переименуйте его в `credentials.json` и поместите в папку `/google_api/`
3. Запустите `main.py`
4. После того, как у вас откроется бразуер (если нет - смотрите ссылку в консоли) и залогиньтес с аккаунта, на котором настраивали API из первого пункта этого раздела
5. Если у вас создался файл `/google_api/token.json` - всё гуд. Если нет - что-то не так с `credentials.json`

## Шаг 3 - балуемся с цифрами, чтобы проверить работу
1. В самом конце инструкции будет валяться ссылка на Spreadsheet. Делайте копию, копию к себе и копируйте ID из URL на таблицу.
2. Вставьте полученный ID в `settings.py` (вы увидите куда)
3. Меняйте `NOTIFICATION_CHECK_INTERVAL` с 20 секунд на больше, чем `ВАШЕ_ВРЕМЯ_В_СЕКУНДАХ`, чтобы бот сразу вам написал. А так он пишет только в полуночь - так задумано. Лучшего вариант в за пару дней не написать при таком задании :)
4. Команды бота:
 * `/addusernotification`,`/aun`,`/add` - добавляет ID чата в `bot_data/notification_list.csv`
 * `/removeusernotification`,`/run`,`/remove` - убирает ID чата из `bot_data/notification_list.csv`

## Шаг 4 - создание Docker-контейнера
1. Откройте `Dockerfile` и вставьте токен для телеграм бота в строке
```docker
ENV TELEGRAM_BOT_TOKEN="PLACE_YOUR_TOKEN_HERE" 
```
2. Откройте терминал и пропишите
```bash
docker-compose up
```
3. После установки и всяких перехеширований - докер запустит сразу два контейнера - один PostgreSQL, другой - само приложение (хост). Подробнее об образах гляньте в `docker-compose.yml`
4. Чтобы глянуть на данные в таблице - откройте контейнер с PostgreSQL - он же `database` и пишите вместе со мной и у вас выведется:
```bash
psql -U postgres -W -p 5432 -h localhost
Password: postgres
# psql (14.4 (Debian 14.4-1.pgdg110+1))
# Type "help" for help.

postgres=# \c canalservice
Password: postgres
You are now connected to database "canalservice" as user "postgres".
canalservice=# select * from orders LIMIT 10;
 nn | order_id | usd_value |    delivery_date    |  rub_value  
----+----------+-----------+---------------------+-------------
  1 | 1249708  |       675 | 2022-05-24 00:00:00 |  39002.9175
  2 | 1182407  |       214 | 2022-05-13 00:00:00 |  12365.3694
  3 | 1120833  |       610 | 2022-05-05 00:00:00 |   35247.081
  4 | 1060503  |      1804 | 2022-05-29 00:00:00 | 104238.9084
  5 | 1617397  |       423 | 2022-05-26 00:00:00 |  24441.8283
  6 | 1135907  |       682 | 2022-05-02 00:00:00 |  39407.3922
  7 | 1235370  |      1330 | 2022-05-05 00:00:00 |   76850.193
  8 | 1329994  |       646 | 2022-07-21 00:00:00 |  37327.2366
  9 | 1876515  |      1335 | 2022-07-22 00:00:00 |  77139.1035
 10 | 1835607  |      1227 | 2022-07-23 00:00:00 |  70898.6367
(10 rows)

canalservice=# 
```
5. Меняйте даты или данные в вашем Spreadsheet, а затем заново смотрите данные в базе данных - они должны меняться. Хотя сама программа, если что, выводит последние несколько строк как `print(df.tail)`, но для подстраховки глянете так.

Spreadsheet link (allow to read for all for now): https://docs.google.com/spreadsheets/d/1ogdQQD10AM2cBwprYhm-Oh4oAeFzfaoQAgsfYCXwzkQ/edit?usp=sharing