import sqlite3

conn = sqlite3.connect('NEW.sqlite')
cur = conn.cursor()

title = input("title: ")
url = input("url: ")

cur.execute('INSERT INTO Статьи (title, url) VALUES (?, ?)', [title, url])
conn.commit()
