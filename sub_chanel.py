def check_sub_chanel(chat_member):
    if chat_member.status != 'left':
        return True
    return False


def hello(username):
    return f'Привет {username}, меня зовут MozgBot. Готов ответить на любой твой вопрос в одной из 4 ролей.' \
               f' Для начала выбери от чьего лица хочешь получить ответ.'
