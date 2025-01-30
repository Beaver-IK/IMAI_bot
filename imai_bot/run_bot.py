import os
import requests
import json
from dotenv import load_dotenv
from telebot import TeleBot
import sqlite3

load_dotenv()


TELEGRAM_TOKEN=os.getenv('TELEGRAM_TOKEN')

SENDBOX_TOKEN=os.getenv('SENDBOX_TOKEN')

ENDPOINT = 'https://api.imeicheck.net/v1/checks'

bot = TeleBot(token=TELEGRAM_TOKEN)


def get_answer(data):
    answer = str()
    for key, value in data.items():
        answer += f'{key}: {value} \n'
    return answer

def get_imei(imei):
    payload = json.dumps(dict(
        deviceId=imei,
        serviceId=12)
    )
    headers = {
    'Authorization': 'Bearer ' + SENDBOX_TOKEN,
    'Accept-Language': 'ru',
    'Content-Type': 'application/json'
    }

    try:
        response = requests.request('POST',
                                ENDPOINT,
                                headers=headers,
                                data=payload)
    except Exception as e:
        return e
    
    data = json.loads(response.text)
    answer = get_answer(data['properties'])
    return answer

def validation_user(id):
    with sqlite3.connect('db.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM customuser WHERE telegram_id = ?', (id))
        user = cur.fetchone()
        conn.close()
        return user


@bot.message_handler(commands=['start'])
async def wake_up(message):
    chat_id = message.chat.id
    name = message.from_user.first_name
    if validation_user(message.from_user.id):
        bot.send_message(
            chat_id=chat_id,
            text=f'Привет, {name}. Введи интересующий IMEI',
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text=f'Привет, {name}. У тебя нет доступа к сервису',
        )

@bot.message_handler(func=lambda message: True)
def get_imei_info(message):
    imei = message.text
    info = get_imei(imei)
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text=info
    )


def main():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()