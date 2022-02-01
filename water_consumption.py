import random
import sqlite3
from subprocess import STARTF_USESTDHANDLES
from flask import Blueprint, request

from users import get_single_user

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

water_consumption = Blueprint('water_consumption', __name__)

@water_consumption.route('/consumption', methods=['POST'])
def add_consumption():
    conn = get_db_connection()
    data = request.get_json(force=True)
    consumption = data['consumption']
    conn.execute("INSERT INTO water_consumption(consumption) VALUES (?)", (consumption,))
    conn.commit()
    return {"message":"Water consumption inserted successfully!"}
