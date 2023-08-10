from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import openai
from keyboard_menu import roles_kb, kb, sub, back, buy_subscribe
from aiogram.types.message import ContentType
from DataBase import check_user, add_pay_user, get_description, change_role, get_role, add_user, check_month, \
    check_is_admin, list_of_users
from sub_chanel import check_sub_chanel, hello

load_dotenv()

token = os.getenv("BOT_TOKEN")
bot = Bot(token=token)
openai.api_key = os.getenv("API_KEY")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
PASSWORD = os.getenv("PASSWORD")
dp = Dispatcher(bot)
CHANNEL_ID = '@my_test_bot18'
PHOTOS = []

MODEL = 'gpt-3.5-turbo'
PRICE = types.LabeledPrice(label='Подписка на 1 месяц', amount=1000 * 100)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    name = message.chat.username
    uid = message.from_user.id
    add_user(uid)
    response = hello(name)
    await bot.send_message(message.chat.id, text=response, reply_markup=kb)
    await message.delete()


@dp.callback_query_handler(text='Вернуться в меню')
async def restart(call: types.CallbackQuery):
    name = call.from_user.username
    response = hello(name)
    await call.message.answer(text=response, reply_markup=kb)


@dp.callback_query_handler(text=['Подписка'])
async def subscribe(call: types.CallbackQuery):
    await call.message.answer('Вы покупаете подписку на месяц, и можете отправлять боту 100 сообщений!',
                              reply_markup=sub)


@dp.callback_query_handler(text=['Роли'])
async def roles(call: types.CallbackQuery):
    await call.message.answer(text='Выберите одну из ролей, в которой вам ответит бот', reply_markup=roles_kb)


@dp.callback_query_handler(text=['Гопник', 'Жириновский', 'Дмитрий Пучков', 'ChatGPT'])
async def all_roles(call: types.CallbackQuery):
    change_role(call.from_user.id, call.data)
    await call.message.answer(text=f'Роль успешно изменена на {call.data}. {get_description(call.data)}')
    await call.message.answer(text='Введите свой вопрос')


@dp.message_handler(content_types=['document', 'sticker', 'photo'])
async def photo(message: types.Message):
    global PHOTOS
    uid = message.from_user.id
    if check_is_admin(uid):
        if message.photo:
            PHOTOS.append(message.photo[0]['file_id'])
            await bot.send_message(message.chat.id, 'принято')
        else:
            await bot.send_message(message.chat.id, 'Рассылка принимает только фото')
    else:
        await bot.send_message(message.chat.id, 'Бот не принимает стикеры, документы и фото')


@dp.callback_query_handler(text=['Купить'])
async def buy_sub(call: types.CallbackQuery):
    if PAYMENT_TOKEN.split(":")[1] == 'TEST':
        await call.message.answer(text="Тестовый платеж")
    await bot.send_invoice(call.message.chat.id,
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
    user_id = message.from_user.id
    add_pay_user(user_id)
    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100}"
                           f" {message.successful_payment.currency} прошел успешно")


@dp.message_handler()
async def get_all_messages(message: types.Message):
    global PHOTOS
    user_id = message.from_user.id
    CUR_ROLE = get_role(user_id)
    text = message.text.split(':')
    if text[0] != PASSWORD:
        if check_month(user_id):
            if CUR_ROLE:
                if check_sub_chanel(await bot.get_chat_member(chat_id=-1001928881431, user_id=user_id)):
                    if check_user(user_id):
                        msg = await bot.send_message(message.chat.id, 'Обработка запроса')
                        response = openai.ChatCompletion.create(
                            model=MODEL,
                            temperature=0.5,
                            messages=[
                                {'role': 'system',
                                 'content': f'Отвечай как будто ты {CUR_ROLE} и не выходи из этой роли'
                                            'К тебе обратился пользователь с таким сообщением.'
                                            ' В конце каждого'
                                            'сообщения ты подписываешься. Что ему ответить?'},
                                {'role': 'user', 'content': message.text}
                            ],
                            max_tokens=500,
                        )
                        answer = response.choices[0].message.content
                        await msg.delete()
                        await bot.send_message(message.chat.id, answer, reply_markup=back)
                        await message.delete()
                    else:
                        await bot.send_message(message.chat.id,
                                               text="Вы исчерпали свой месячный лимит по данной подписке",
                                               reply_markup=buy_subscribe)
                else:
                    await bot.send_message(message.chat.id,
                                           f'Для того чтобы обращаться к боту подпишитесь на канал {CHANNEL_ID}')
            else:
                await bot.send_message(message.chat.id, text='Сначала выберите роль', reply_markup=roles_kb)
        else:
            await bot.send_message(message.chat.id, text="Ваша предыдущая подписка закончилась\n"
                                                         "для продолжения оплатите подписку за данный месяц",
                                   reply_markup=sub)
    else:
        for i in list_of_users():
            if PHOTOS:
                for j in PHOTOS:
                    await bot.send_photo(i, j)
            await bot.send_message(i, text[1])
        PHOTOS = []


executor.start_polling(dp, skip_updates=False)
