import os, sqlite3

# Level System DB Recreate
# Created : 23.12.31
# Modified : 24.02.12

db_path = 'level.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (userid TEXT PRIMARY KEY, count INTEGER, level INTEGER)''')
print("Recreated")
conn.close()