import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (name, height, hair_length) VALUES (?, ?, ?)",
            ('Default user', '180', 'short')
            )

cur.execute("INSERT INTO dispenser (fill_value) VALUES(?)", ('100',))

cur.execute("INSERT INTO water(temperature, preparation_date) VALUES (?, ?)", ('23','01/30/22'))

connection.commit()
connection.close()