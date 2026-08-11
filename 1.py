import sqlite3

db = sqlite3.connect("todo.db")
cursor = db.cursor()

cursor.execute("DELETE FROM notification WHERE id = 1")

db.commit()
db.close()