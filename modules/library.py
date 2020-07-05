import telebot


class Library:

    text = None
    text_length = 0
    custom_buttons = None

    def __init__(self, bot):

        self.bot = bot

        @bot.callback_query_handler(func=lambda c: c.data[:8] == 'to_text_')
        def _updater(query):
            Library.updater(self, query)

    def builder(self, query: telebot.types.Message, text: str, custom_buttons: list = None):

        self.text = text
        self.custom_buttons = custom_buttons
        self.text_length = len(text)

        if type(query) == telebot.types.Message:
            chat_id = query.chat.id
        elif type(query) == telebot.types.CallbackQuery:
            chat_id = query.message.chat.id

        keyboard = Library.create_nav(
            self=self,
            start=0,
            stop=700
        )

        self.bot.send_message(
            chat_id,
            text[:700],
            parse_mode='Markdown',
            reply_markup=keyboard)

    def updater(self, query: telebot.types.Message):

        self.bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=self.text[int(query.data[8:]):int(query.data[8:]) + 700],
            parse_mode='Markdown',
            reply_markup=Library.create_nav(
                self=self,
                start=int(query.data[8:]),
                stop=int(query.data[8:]) + 700
            )
        )

    def create_nav(self, start: int, stop: int):

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)

        buttons_ = []

        if start > 0:
            buttons_.append(telebot.types.InlineKeyboardButton(text='⬅', callback_data='to_text_{}'.format(start - 700)))
        if stop < self.text_length:
            buttons_.append(telebot.types.InlineKeyboardButton(text='➡', callback_data='to_text_{}'.format(stop)))

        keyboard.add(*buttons_)

        if self.custom_buttons is not None:
            for row in self.custom_buttons:
                keyboard.row(*row)

        return keyboard

