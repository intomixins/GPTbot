import sqlite3
from types import NoneType
from datetime import date


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
            if count <= 10:
                cur.execute(f"UPDATE users SET count = count + 1 WHERE user_id == {user_id}")
            else:
                return 'limit'


def list_of_users():
    with sqlite3.connect('bot.db') as conn:
        cur = conn.cursor()
        lst = cur.execute(f"SELECT user_id FROM users").fetchall()
        return list([i[0] for i in lst])


def add_user(user_id):
    if user_id not in list_of_users():
        with sqlite3.connect('bot.db') as conn:
            cur = conn.cursor()
            cur.execute(f"INSERT INTO users VALUES({user_id}, 0, 0, 1, 0, NULL)")


def check_user(user_id):
    if not new_message(user_id):
        return True
    return False


def add_pay_user(user_id):
    with sqlite3.connect('bot.db') as conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE users SET count = 0, is_member = 1, date = '{date.today()}'")


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


def change_role(user_id, role):
    with sqlite3.connect('bot.db') as conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE users SET role_id = {get_id_by_name(role)} WHERE user_id = {user_id}")


def get_role(user_id):
    with sqlite3.connect('bot.db') as conn:
        cur = conn.cursor()
        role_id = cur.execute(f"SELECT role_id FROM users WHERE user_id = {user_id}").fetchone()[0]
        if role_id != 0:
            return cur.execute(f"SELECT name FROM roles WHERE id = {role_id}").fetchone()[0]
        return None


def check_month(user_id):
    with sqlite3.connect('bot.db') as conn:
        cur = conn.cursor()
        year, month, day = cur.execute(f"SELECT date FROM users WHERE user_id = {user_id}").fetchone()[0].split('-')
        if date.today().year == int(year) and date.today().month == int(f"{(int(month) + 1):02}") \
                and date.today().day == int(day):
            return False
    return True
