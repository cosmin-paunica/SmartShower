import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

users_to_insert = [
    ('Default user', '180', 'short'),
    ('Savannah Britton', '162', 'long'),
    ('Rachel Hester', '175', 'long'),
    ('Connor Evans', '192', 'long'),
    ('Khloe Irvine', '182', 'short'),
    ('Efan Olsen', '168', 'short')
]
cur.executemany("INSERT INTO users (name, height, hair_length) VALUES (?, ?, ?)", users_to_insert)

fill_value_to_insert = [
    ('95',),
    ('90',),
    ('85',),
    ('75',),
    ('70',),
    ('66',),
    ('62',),
    ('54',),
    ('100',)
]
cur.executemany("INSERT INTO dispenser (fill_value) VALUES(?)", fill_value_to_insert)

water_to_insert = [
    ('32','01/15/22'),
    ('32.5','01/16/22'),
    ('31','01/17/22'),
    ('31','01/18/22'),
    ('32.5','01/20/22'),
    ('32','01/21/22'),
    ('29.5','01/23/22'),
    ('29.5','01/24/22'),
    ('31.5','01/25/22')
]
cur.executemany("INSERT INTO water(temperature, preparation_date) VALUES (?, ?)", water_to_insert)

water_consumption_to_insert = [ # 37 - 94 L / 5 min
    ('45.3',),
    ('38.1',),
    ('40.5',),
    ('42.4',),
    ('39.5',),
    ('44.7',),
    ('54.6',),
    ('52.1',),
    ('47.6',)
]
cur.executemany("INSERT INTO water_consumption(consumption) VALUES (?)", water_consumption_to_insert)

connection.commit()
connection.close()