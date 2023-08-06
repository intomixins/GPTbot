import sqlite3


def new_message(user_id):
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        lst = cur.execute(f"SELECT is_member, count FROM users WHERE user_id = {user_id}").fetchall()
        is_member, count = lst[0][0], lst[0][1]
        if is_member == 1:
            if count < 100:
                cur.execute(f"UPDATE users SET count = count + 1 WHERE user_id == {user_id}")
            else:
                return 'limit'
        else:
            if count < 10:
                cur.execute(f"UPDATE users SET count = count + 1 WHERE user_id == {user_id}")
            else:
                return 'limit'


def list_of_users():
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        lst = cur.execute(f"SELECT user_id FROM users").fetchall()
        return list([i[0] for i in lst])


def add_user(user_id):
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO users VALUES({user_id}, 0, 0, 0)")


def check_user(user_id):
    if user_id in list_of_users():
        if not new_message(user_id):
            return True
        return False
    add_user(user_id)
    return True


