import random
from db_conn import get_db_connection
from subprocess import STARTF_USESTDHANDLES
from flask import Blueprint, request

from users import get_single_user

water_consumption = Blueprint('water_consumption', __name__)

@water_consumption.route('/consumption', methods=['POST'])
def add_consumption():
    conn = get_db_connection()
    data = request.get_json(force=True)
    consumption = data['consumption']
    conn.execute("INSERT INTO water_consumption(consumption) VALUES (?)", (consumption,))
    conn.commit()
    return {"message":"Water consumption inserted successfully!"}
