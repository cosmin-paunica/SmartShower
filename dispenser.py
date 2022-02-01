from db_conn import get_db_connection
from flask import Blueprint, request

from users import get_single_user


dispenser = Blueprint('dispenser', __name__)

@dispenser.route('/dispenser', methods=['GET'])
def get_fill_value():
    conn = get_db_connection()
    rows = conn.execute('SELECT MAX(id), fill_value FROM dispenser GROUP BY id').fetchall()
    result = {}
    for row in rows:
        result = dict(row)  #TODO: find something that looks better
    result.pop('MAX(id)', None)
    conn.close()
    return result

@dispenser.route('/dispenser', methods=['PUT'])
def use_dispenser():
    data = request.get_json(force=True)
    name = data['name']
    fill_value = get_fill_value()['fill_value']

    user = get_single_user(name)
    if user['hair_length'] == 'short':
        hair_coefficient = 1
    elif user['hair_length'] == 'medium':
        hair_coefficient = 2
    else: 
        hair_coefficient = 3

    new_fill_value = fill_value - user['height'] * 0.05 - hair_coefficient
    conn = get_db_connection()
    conn.execute('INSERT INTO dispenser (fill_value) VALUES (?)', (new_fill_value,)).fetchall()
    conn.commit()
    conn.close()
    return {"message":"Dispenser successfully used!"}

@dispenser.route('/dispenser', methods=['POST'])
def fill_dispenser():
    conn = get_db_connection()
    conn.execute('INSERT INTO dispenser (fill_value) VALUES (?)', (100,)).fetchall()
    conn.commit()
    conn.close()
    return {"message":"Dispenser successfully filled!"}
