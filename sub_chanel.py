def check_sub_chanel(chat_member):
    if chat_member.status != 'left':
        return True
    return False

