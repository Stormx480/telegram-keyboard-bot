import telebot


class Gallery:

    pictures = None
    len = 0
    custom_buttons = None

    def __init__(self, bot):

        self.bot = bot

        @bot.callback_query_handler(func=lambda c: c.data[:11] == 'to_picture_')
        def _updater(query):
            Gallery.updater(self, query)

    def builder(self, query: telebot.types.Message or telebot.types.CallbackQuery, pictures: list,
                custom_buttons: list = None):

        self.custom_buttons = custom_buttons
        self.pictures = pictures
        self.len = len(pictures)

        if self.len == 0:
            raise Exception('Pictures list is empty')

        if type(query) == telebot.types.Message:
            chat_id = query.chat.id
        elif type(query) == telebot.types.CallbackQuery:
            chat_id = query.message.chat.id

        nav = Gallery.create_nav(self, 0, 1, self.len)

        self.bot.send_photo(
            chat_id=chat_id,
            photo=pictures[0],
            reply_markup=nav
        )

    def updater(self, query: telebot.types.Message):

        self.bot.edit_message_media(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            media=telebot.types.InputMediaPhoto(self.pictures[int(query.data[11:])]),
            reply_markup=Gallery.create_nav(self, int(query.data[11:]), int(query.data[11:])+1, pictures_len=self.len))

    def create_nav(self, start: int, stop: int, pictures_len: int):

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)

        buttons_ = []

        if start > 0:
            buttons_.append(telebot.types.InlineKeyboardButton(text='⬅', callback_data='to_picture_{}'.format(start - 1)))
        if stop < pictures_len:
            buttons_.append(telebot.types.InlineKeyboardButton(text='➡', callback_data='to_picture_{}'.format(stop)))

        keyboard.add(*buttons_)

        if self.custom_buttons is not None:
            for row in self.custom_buttons:
                keyboard.row(*row)

        return keyboard
