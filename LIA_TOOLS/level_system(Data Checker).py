import sqlite3

# Level System Data Checker (CUI)
# Created : 23.12.31

conn = sqlite3.connect('level.db')
c = conn.cursor()
c.execute('SELECT * FROM users')
rows = c.fetchall()

for row in rows:
    print(row)

conn.close()
