from db_conn import get_db_connection
from subprocess import STARTF_USESTDHANDLES
from flask import Blueprint, request

from users import get_single_user



water = Blueprint('water', __name__)

@water.route('/water/temperature', methods=['GET'])
def get_water_params():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM water ORDER BY id DESC').fetchone()
    result = dict(rows)
    
    conn.close()
    return result

@water.route('/water/temperature', methods=['PUT'])
def set_water_params():
    conn = get_db_connection()
    data = request.get_json(force=True)
    new_temp = data['temperature']
    new_date = data['preparation_date']
    rows = conn.execute('INSERT INTO water(temperature, preparation_date) VALUES (?,?)', (new_temp, new_date)).fetchall()
    conn.commit()
    conn.close()
    return {'message':'Watter parameters added successfully!'}

@water.route('/water/consumption', methods=['POST'])
def add_consumption():
    conn = get_db_connection()
    data = request.get_json(force=True)
    consumption = data['consumption']
    conn.execute("INSERT INTO water_consumption(consumption) VALUES (?)", (consumption,))
    conn.commit()
    return {"message":"Water consumption inserted successfully!"}
