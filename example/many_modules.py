import telebot

from config import token
from modules.gallery import Gallery
from modules.library import Library
from modules.keyboards import InlineKeyboard


class Bot(Gallery, Library):

    bot = telebot.TeleBot(token)

    pictures = ['url or photo_file_id']

    with open('text.txt', 'r') as file:
        text = file.read()

    def __init__(self):
        """
        For multiple inheritance of modules, each module must be init explicitly.
        Use the class name for this.
        To call the 'builder' function, module must also be specified explicitly.
        InlineKeyboard and Keyboard modules don't need to init class for call 'builder' function.
        """
        Gallery.__init__(self, self.bot)
        Library.__init__(self, self.bot)

        @self.bot.message_handler(commands=['start'])
        def welcome(query):
            """We create Inline Keyboard at /start, to select the module that we want to see."""
            InlineKeyboard.builder(query, message='Hello! Choose which module you want to see?', buttons=['Gallery', 'Library'])

        @self.bot.callback_query_handler(func=lambda query: query.data == 'Gallery')
        def gallery(query):
            """We create a gallery object with custom buttons for navigation."""
            custom_buttons = [
                (telebot.types.InlineKeyboardButton(text='Library', callback_data='Library'),)
            ]
            Gallery.builder(self, query=query, pictures=self.pictures, custom_buttons=custom_buttons)

        @self.bot.callback_query_handler(func=lambda query: query.data == 'Library')
        def library(query):
            """We create a library object with custom buttons for navigation."""
            custom_buttons = [
                (telebot.types.InlineKeyboardButton(text='Gallery', callback_data='Gallery'),)
            ]
            Library.builder(self, query=query, text=self.text, custom_buttons=custom_buttons)


if __name__ == '__main__':
    Bot().bot.polling()
