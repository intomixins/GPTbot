from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

kb = InlineKeyboardMarkup()
kb1 = InlineKeyboardButton(text='Подписка', callback_data='Подписка')
kb2 = InlineKeyboardButton(text='Роли', callback_data='Роли')
kb.row(kb1, kb2)


sub = InlineKeyboardMarkup()
sub1 = InlineKeyboardButton(text='Купить подписку', callback_data='Купить')
sub2 = InlineKeyboardButton(text='Вернуться в меню', callback_data='Вернуться в меню')
sub.add(sub1, sub2)

roles_kb = InlineKeyboardMarkup()
r1 = InlineKeyboardButton(text='Гопник', callback_data="Гопник")
r2 = InlineKeyboardButton(text='Жириновский', callback_data='Жириновский')
r3 = InlineKeyboardButton(text='Гоблин Пучков', callback_data='Гоблин Пучков')
r4 = InlineKeyboardButton(text='Илон Маск', callback_data='Илон Маск')
roles_kb.add(r1, r2)
roles_kb.row(r3, r4)


back = InlineKeyboardMarkup()
b1 = InlineKeyboardButton(text='Вернуться в меню', callback_data='Вернуться в меню')
back.add(b1)


buy_subscribe = InlineKeyboardMarkup()
bs1 = InlineKeyboardButton(text='Купить подписку', callback_data='Купить')
buy_subscribe.add(bs1)
