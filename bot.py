import requests
import time
import telebot
from dotenv import load_dotenv
import os

load_dotenv()
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
TEXTRU_API_KEY = os.getenv('TEXTRU_API_KEY')

bot = telebot.TeleBot(BOT_API_TOKEN)

user_states = {}

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """Привет, уверен что вы сталкивались с тем что разные сайты выдают разные результаты проверки на уникальность.
    
Этот бот используя разные алгоритмы проверки текста на уникальность даст вам наиболее полную картину уникальности вашего текста
Используйте команду /unique, чтобы я начал прверять на уникальность все ваши сообщения.""")

@bot.message_handler(commands=['unique'])
def include_text(message):
    bot.reply_to(message, "Проверка на уникальность запущена. Все послейдующие сообщения будут проходить проверку.\nЧтобы остановить проверку напишите воспользуйтесь командой /stop")
    user_id = message.from_user.id
    user_states[user_id] = True
    print(1)

@bot.message_handler(commands=['stop'])
def stop_unique(message):
    user_id = message.from_user.id
    user_states[user_id] = False
    print(2)
    bot.send_message(message.chat.id, "Проверка на уникальность остановлена, чтобы возобновить проверку используйте команду /unique")

@bot.message_handler(func=lambda text: True)
def unique_text(message):
    user_id = message.from_user.id
    if user_id in user_states and user_states[user_id]:
        print(message.text)
        unique_textru = get_unique_textru(message.text)
        if unique_textru:
            bot.reply_to(message, unique_textru)
        else:
            bot.reply_to(message, "Извините у нас технические шоколадки...")
    else:
        bot.reply_to(message, "Используйте команду /unique, чтобы я начал прверять yf уникальность все ваши сообщения.")


def checking_text_for_uniqueness(text):
    url_sumbit = "http://api.text.ru/post"
    data_submit = {
        'text': text,
        'userkey': TEXTRU_API_KEY
    }

    response = requests.post(url_sumbit, data=data_submit)

    if response.status_code == 200:
        json_response = response.json()
        print(json_response)
        if 'text_uid' in json_response:
            return json_response['text_uid']
        else:
            print('Eror:', json_response)
            return None
    else:
        print('HTTP Eror:', response.status_code)
        return None


def get_result(text_uid):
    url_result = 'http://api.text.ru/post'

    data_result = {
        'uid': text_uid,
        'userkey': TEXTRU_API_KEY
    }

    time.sleep(5)
    while True:
        response = requests.post(url_result, data_result)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json, type(response_json))
            if 'text_unique' in response_json:
                return response_json['unique']
            elif 'error_code' in response_json:
                print("Ошибка:", response_json['error_desc'])
                time.sleep(3)
        else:
            print('HTTP Eror:', response.status_code)
            time.sleep(3)

def get_unique_textru(text):
    uid = checking_text_for_uniqueness(text)
    if uid:
        unique_text = get_result(uid)
        return unique_text
    else:
        return None


bot.infinity_polling()