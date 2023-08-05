from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import openai
from keyboard_menu import kb_menu, sub_menu, role_menu
from asyncio import run

load_dotenv()

token = os.getenv("BOT_TOKEN")
bot = Bot(token=token)
openai.api_key = os.getenv("API_KEY")
dp = Dispatcher(bot)

MODEL = 'gpt-3.5-turbo'
ROLES = ['гопник', 'Владимир Жириновский']
CUR_ROLE = ''
COUNTER = 0


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    name = message.chat.username
    uid = message.from_user.id
    response = f'Привет {name}, {uid}, меня зовут MozgBot. Готов ответить на твои вопросы.' \
               f' Для начала напиши от чьего лица хочешь получить ответ.'
    await bot.send_message(message.chat.id, text=response, reply_markup=kb_menu)


def subscribe(message: types.Message):
    print(message.text)


def roles(message: types.Message):
    pass


@dp.message_handler()
async def get_all_messages(message: types.Message):
    if message.text == 'Роли':
        return roles(message)
    if message.text == 'Подписка':
        return subscribe(message)

    global CUR_ROLE, COUNTER
    if message.text in ROLES:
        CUR_ROLE = message.text
        await bot.send_message(message.chat.id, 'Введите свой вопрос')
        return
    response = openai.ChatCompletion.create(
        model=MODEL,
        temperature=0.5,
        messages=[
            {'role': 'system', 'content': f'Отвечай как будто ты {CUR_ROLE} и не выходи из этой роли'
                                          'К тебе обратился пользователь с таким сообщением.'
                                          ' В конце каждого'
                                          'сообщения ты подписываешься. Что ему ответить?'},
            {'role': 'user', 'content': message.text}
        ],
        max_tokens=500,
    )
    answer = response.choices[0].message.content
    await bot.send_message(message.chat.id, answer)


executor.start_polling(dp)
