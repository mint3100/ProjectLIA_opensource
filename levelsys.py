import sqlite3

# Level System Database Function
# Created : 23.12.31

conn = sqlite3.connect('level.db')
cursor = conn.cursor()

print("[alert] LevelSys Module Load Complete")

def levels(userid):
    global count
    global updated_count
    global level
    global updated_level
    updated_level = 0
    cursor.execute("SELECT count, level FROM users WHERE userid=?", (userid,))
    result = cursor.fetchone()

    if result:
        count = result[0]
        level = result[1]
        updated_count = count + 1
        if updated_count % 10 == 0:
            updated_level = level + 1
            cursor.execute("UPDATE users SET count=?, level=? WHERE userid=?", (updated_count, updated_level, userid))
            conn.commit()
        else:
            cursor.execute("UPDATE users SET count=? WHERE userid=?", (updated_count, userid))
            conn.commit()
    else:
        count = 0
        level = 1
        cursor.execute("INSERT INTO users (userid, count, level) VALUES (?, ?, ?)", (userid, count, level))
        conn.commit()

def data_check(userid):
    global result
    conn = sqlite3.connect('level.db')
    cursor = conn.cursor()
    cursor.execute("SELECT count, level FROM users WHERE userid=?", (userid,))
    result = cursor.fetchone()
    conn.close()

def db_close():
    conn.close()