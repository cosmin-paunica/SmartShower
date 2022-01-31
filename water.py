import sqlite3
from subprocess import STARTF_USESTDHANDLES
from flask import Blueprint, request

from users import get_single_user

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

water = Blueprint('water', __name__)

@water.route('/water', methods=['GET'])
def get_water_params():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM water ORDER BY id DESC').fetchone()
    result = dict(rows)
    
    conn.close()
    return result

@water.route('/water', methods=['PUT'])
def set_water_params():
    conn = get_db_connection()
    data = request.get_json(force=True)
    new_temp = data['temperature']
    new_date = data['preparation_date']
    rows = conn.execute('INSERT INTO water(temperature, preparation_date) VALUES (?,?)', (new_temp, new_date)).fetchall()
    conn.commit()
    conn.close()
    return {'message':'success'}

