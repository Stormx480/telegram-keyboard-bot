import telebot
from config import token

bot = telebot.TeleBot(token)


class Keyboard:

    @staticmethod
    def builder(query: telebot.types.Message, buttons: list, row_width: int = 1, message: str = None):

        markup = telebot.types.ReplyKeyboardMarkup(row_width=row_width)

        buttons_ = list(map(lambda button: telebot.types.KeyboardButton(button), buttons))

        markup.add(*buttons_)

        bot.send_message(query.chat.id, message, reply_markup=markup)


class InlineKeyboard:

    @staticmethod
    def builder(query: telebot.types.Message, buttons: list, row_width: int = 1, message: str = None):

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=row_width)

        buttons_ = list(map(lambda button: telebot.types.InlineKeyboardButton(button, callback_data=button), buttons))

        keyboard.add(*buttons_)

        bot.send_message(query.chat.id,
                         message,
                         reply_markup=keyboard,
                         parse_mode='Markdown'
                         )
