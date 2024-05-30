import sqlite3 as sq


def init_db():
    with sq.connect("bot_users.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS bot_users (
        tgUserId INTEGER PRIMARY KEY NOT NULL,
        isChecking INTEGER DEFAULT 0
        )""")
        con.commit()

def init_new_user(tg_user_id, is_checking = False):
    with sq.connect("bot_users.db") as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO bot_users (tgUserId, isChecking) VALUES ({tg_user_id}, {is_checking})")
        con.commit()

def set_user_state(tg_user_id, is_checking):
    with sq.connect("bot_users.db") as con:
        cur = con.cursor()
        cur.execute(f"UPDATE bot_users SET isChecking = {is_checking} WHERE tgUserId == {tg_user_id}")
        print()
        con.commit()


def get_user_state(tg_user_id) -> bool:
    with sq.connect("bot_users.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT isChecking FROM bot_users WHERE tgUserId == {tg_user_id}")
        result = cur.fetchone()[0]
        print(result)
        return result


