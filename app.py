from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import openai
from keyboard_menu import kb_menu, sub_menu, role_menu
from aiogram.types.message import ContentType
from DataBase import check_user
from sub_chanel import check_sub_chanel

load_dotenv()

token = os.getenv("BOT_TOKEN")
bot = Bot(token=token)
openai.api_key = os.getenv("API_KEY")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
dp = Dispatcher(bot)
CHANNEL_ID = '@my_test_bot18'

MODEL = 'gpt-3.5-turbo'
ROLES = ['гопник', 'Владимир Жириновский']
CUR_ROLE = ''
PRICE = types.LabeledPrice(label='Подписка на 1 месяц', amount=1000 * 100)


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


@dp.message_handler(commands=['Купить'])
async def buy(message: types.Message):
    if PAYMENT_TOKEN.split(":")[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж", reply_markup=kb_menu)

    await bot.send_invoice(message.chat.id,
                           title='Подписка на бота',
                           description='Активация на один месяц',
                           provider_token=PAYMENT_TOKEN,
                           currency='rub',
                           photo_url='https://telegram.org/file/464001533/1130b/LOLHYtTvIyg.5632468/765938e39b6572ef3c',
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter='one-month-subscription',
                           payload='test-invoice-payload')


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100}"
                           f" {message.successful_payment.currency} прошел успешно")


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
            await bot.send_message(message.chat.id,
                                   f'Для того чтобы обращаться к боту подпишитесь на канал {CHANNEL_ID}')
    else:
        await bot.send_message(message.chat.id, text="Вы исчерпали свой месячный лимит по данной подписке")


executor.start_polling(dp, skip_updates=False)
