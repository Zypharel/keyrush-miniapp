import sqlite3

with open("keyrush_market.sql", "r", encoding="utf-8") as f:
    sql = f.read()

conn = sqlite3.connect("keyrush_market.db")
cursor = conn.cursor()
cursor.executescript(sql)
conn.commit()
conn.close()

print("База данных успешно создана!")
