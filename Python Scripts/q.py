import sqlite3

conn = sqlite3.connect('NEW.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Статьи')
rows = cur.fetchone()

print(rows)
