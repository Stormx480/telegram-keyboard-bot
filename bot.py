# -*- coding: utf-8 -*-
import telebot

import logging
import ssl

from telebot import types #Если вы используете bot.pooling() на стадии разработки и живете в России,
                          #то не забудьте импортировать модуль apihelper для использования прокси.

from config import token # Лучше вынести токен в отдельную переменную в отдельном файле и постоянно его импортировать. Он еще понадобится.
from keyboard import * # При небольшом приложении лучше импортировать класс.
from inline_keyboard import *

from aiohttp import web

API_TOKEN = token

WEBHOOK_HOST = 'ip/domen' #Подставьте IP/domen вашего сервера
WEBHOOK_PORT = 8443 #Вебхуки используют один из портов: 8443, 443, 80, 88. Используемый порт должен быть открыт.
WEBHOOK_LISTEN = '0.0.0.0' #При использовании некоторых VPS серверов нужно указать свой IP

WEBHOOK_SSL_CERT = './webhook_cert.pem' #Путь до SSL сертификата.
WEBHOOK_SSL_PRIV = './webhook_pkey.pem' #Путь до приватного SSL ключа.

#Если у вас нет SSL сертификата, его можно создать (самоподписанный), команды:
#openssl genrsa -out webhook_pkey.pem 2048
#openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#В поле "Common Name (e.g. server FQDN or YOUR name)" укажите такое же значение как и в WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = web.Application()

async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)

app.router.add_post('/{token}/', handle)



@bot.message_handler(commands=['start']) #Обработчик сообщений. В данной строке команды start. Больше об декораторах можете узнать в офф. документации.
def welcome(message):
    Keyboard.start_keyboard(message)#Ссылаемся на функцию start_keyboard в файле keyboard.py. Это удобнее чем расписывать все в одном файле.
                                #Не забудьте передать аргумет Message, иначе функция не сработает.

@bot.message_handler(regexp = 'Simple Keyboard') # regexp - ловит регулярные выражения.
def button_one(message):
    Keyboard.button_one_keyboard(message)

@bot.message_handler(regexp = 'Back to main menu') #Кнопку "Назад" можно сделать по разному. Это самый простой способ.
def back_button(message):
    Keyboard.start_keyboard(message)

@bot.message_handler(regexp = 'Inline Keyboard')# Важное замечание. Не знаю баг это или фича, но если вы сделаете кнопку Keyobard Button и Keyboard Inline и обработчики для них, и в коде хэндлер для Keyboard Button стоит выше, то при нажатии на кнопку Keyboard Inline
#сработает декоратор для Keyboard Button потому что он словит слово Keyboard. Я избежал этого переименованием кнопок, но это неправильный подход. Честно говоря не знаю как это пофиксить,
#пробовал вместо аргумента regexp ставить m.text == 'выражение' но это не сработало. Так же если сделать строгое равенство regexp == 'Keyobard Inline' это не сработает так же.
def button_programm(message):
    InlineKeyboard.button_programm_keyboard(message)

@bot.message_handler(regexp = 'Callback Inline')
def callback(message):
    InlineKeyboard.callback_keyboard(message)

@bot.callback_query_handler(func=lambda c: c.data == 'callback')#Ловим коллбэк от кнопки. Нам передается объект CallbackQuery который содержит поле data и message. Сейчас нам нужно из даты достать наше слово которое мы передали в атрибуте callback_data
def callback_answer(callback_query: types.CallbackQuery): #И отвечаем на него
    bot.answer_callback_query(
            callback_query.id,
            text='Hello! This callback.',
            show_alert=True
            )

#Есть еще switch кнопки, но я их не использовал поэтому их тут нет. В основном они нужны для того что бы обучать пользователей обращению с ботом в iline режиме.


bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=context,
)
