from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, KeyboardButtonPollType

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text='Подписка'),
        KeyboardButton(text='Роли'),
        ]
    ],
    resize_keyboard=True
)

sub_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='купить подписку'),
            KeyboardButton(text='отмена')
        ]
    ]
)

role_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='гопник'),
            KeyboardButton(text='Жириновский'),
            KeyboardButton(text='президент')
        ]
    ]
)

