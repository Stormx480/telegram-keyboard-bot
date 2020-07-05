import telebot
from config import token
from modules.gallery import Gallery


class Bot(Gallery):

    bot = telebot.TeleBot(token)

    pictures = ['<url or photo_file_id>']

    def __init__(self):
        """We init of the inherited class and give him bot object as argument."""
        super().__init__(self.bot)

        @self.bot.message_handler(commands=['start'])
        def start(query):
            """Call Gallery.builder() for create gallery."""
            self.builder(query=query, pictures=self.pictures)


if __name__ == '__main__':

    Bot().bot.polling()
