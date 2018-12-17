# -*- coding: utf-8 -*-
import telebot
from telebot import types
from config import token

bot = telebot.TeleBot(token)

class InlineKeyboard:
    def button_two_keyboard(message):
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(
        text = 'Google', #текст на кнопке
        url = 'https://google.com'
        )
        keyboard.add(url_button)
        bot.send_message(message.chat.id,
        'If you press the button then go to google',
        reply_markup=keyboard
        )

    def callback_keyboard(message):
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(
        text = 'More',
        callback_data = 'callback' #Параметр который вы передаете через callback заполняется в отдельный словарь который вам отправляет сервер. Оно не пишется в чат телеграма.
        )
        keyboard.add(button)
        bot.send_message(message.chat.id,
        'You can use callback inline button in your bot.',
        reply_markup=keyboard
        )
