import sqlite3


def new_message(user_id):
    with sqlite3.connect('bot.db') as conn:
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
    with sqlite3.connect('bot.db') as conn:
        cur = conn.cursor()
        lst = cur.execute(f"SELECT user_id FROM users").fetchall()
        return list([i[0] for i in lst])


def add_user(user_id, cr):
    with sqlite3.connect('bot.db') as conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO users VALUES({user_id}, 0, 0, 1, '{get_id_by_name(cr)}')")


def check_user(user_id, cr):
    if user_id in list_of_users():
        if not new_message(user_id):
            return True
        return False
    add_user(user_id, cr)
    return True


def add_pay_user(user_id, cr):
    with sqlite3.connect('bot.db') as conn:
        cur = conn.cursor()
        if user_id not in list_of_users():
            cur.execute(f"INSERT INTO users VALUES({user_id}, 0, 1, 0, '{get_id_by_name(cr)}')")


def get_description(role_name):
    with sqlite3.connect('bot.db') as conn:
        cur = conn.cursor()
        res = cur.execute(f"SELECT description FROM roles WHERE name = '{role_name}'").fetchone()
        return res[0]


def get_id_by_name(name):
    with sqlite3.connect('bot.db') as conn:
        cur = conn.cursor()
        lst = cur.execute(f"SELECT id FROM roles WHERE name = '{name}'").fetchone()
        return lst[0]


def list_of_roles():
    with sqlite3.connect('bot.db') as conn:
        cur = conn.cursor()
        lst = cur.execute(f"SELECT name FROM roles").fetchall()
        return list([i[0] for i in lst])

