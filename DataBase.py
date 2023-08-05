import sqlite3


def new_message(user_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    lst = cur.execute(f"SELECT is_member, count FROM users WHERE user_id == {user_id}").fetchall()
    is_member, count = lst[0][0], lst[0][1]
    print(is_member, count)
    # if is_member == 1:
    #     if count < 100:
    #         cur.execute(f"UPDATE users SET count = count + 1 WHERE user_id == {user_id}")
    #     else:
    #         return stop_using()
    # else:
    #     if count < 10:
    #         cur.execute(f"UPDATE users SET count = count + 1 WHERE user_id == {user_id}")
    #     else:
    #         return stop_using()


def stop_using():
    return "Вы исчерпали свой месячный лимит"


new_message(826750345)