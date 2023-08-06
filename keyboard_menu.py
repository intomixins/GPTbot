from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, KeyboardButtonPollType

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/Подписка'),
            KeyboardButton(text='/Роли'),
        ]
    ],
    resize_keyboard=True
)

sub_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/Купить'),
            KeyboardButton(text='/Меню')
        ]
    ],
    resize_keyboard=True
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

