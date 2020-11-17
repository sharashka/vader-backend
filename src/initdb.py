import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""CREATE TABLE users
                  (username text,
                  email text,
                  password text,
                  name text,
                  phone text,
                  created_date date)
               """)

cursor.execute("""CREATE TABLE users
                  (username text,
                  email text,
                  password text,
                  name text,
                  phone text,
                  created_date date)
               """)

conn.commit()

users = [('root','root@roten.ru','1111','namename','+79005550055','2020-10-10')]
 
cursor.executemany("INSERT INTO users VALUES (?,?,?,?,?,?)", users)
conn.commit()