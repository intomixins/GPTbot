from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import openai
from keyboard_menu import kb_menu, sub_menu, role_menu
from asyncio import run
from DataBase import check_user
from sub_chanel import check_sub_chanel

load_dotenv()

token = os.getenv("BOT_TOKEN")
bot = Bot(token=token)
openai.api_key = os.getenv("API_KEY")
dp = Dispatcher(bot)

MODEL = 'gpt-3.5-turbo'
ROLES = ['гопник', 'Владимир Жириновский']
CUR_ROLE = ''
CHANNEL_ID = '@my_test_bot18'


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    name = message.chat.username
    uid = message.from_user.id
    response = f'Привет {name}, {uid}, меня зовут MozgBot. Готов ответить на твои вопросы.' \
               f' Для начала напиши от чьего лица хочешь получить ответ.'
    await bot.send_message(message.chat.id, text=response, reply_markup=kb_menu)
    await message.delete()


@dp.message_handler(commands='Подписка')
async def subscribe(message: types.Message):
    await bot.send_message(message.chat.id, text='вся информация о текущей подписке', reply_markup=sub_menu)
    await message.delete()


@dp.message_handler(commands='Роли')
async def roles(message: types.Message):
    await bot.send_message(message.chat.id, text='вся информация о текущей подписке', reply_markup=sub_menu)
    await message.delete()


@dp.message_handler(commands=['Меню'])
async def menu(message: types.Message):
    await bot.send_message(message.chat.id, text='возвращаю тебя в меню', reply_markup=kb_menu)
    await message.delete()


@dp.message_handler()
async def get_all_messages(message: types.Message):
    global CUR_ROLE
    if message.text in ROLES:
        CUR_ROLE = message.text
        await bot.send_message(message.chat.id, 'Введите свой вопрос')
        return
    user_id = message.from_user.id
    if check_user(user_id):
        if check_sub_chanel(await bot.get_chat_member(chat_id=-1001928881431, user_id=user_id)):
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
            await message.delete()
        else:
            await bot.send_message(message.chat.id, f'Для того чтобы обращаться к боту подпишитесь на канал {CHANNEL_ID}')
    else:
        await bot.send_message(message.chat.id, text="Вы исчерпали свой месячный лимит по данной подписке")


executor.start_polling(dp)
