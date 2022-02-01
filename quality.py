import random
import sqlite3
from subprocess import STARTF_USESTDHANDLES
from flask import Blueprint, request

from users import get_single_user

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

quality = Blueprint('quality', __name__)

@quality.route('/quality', methods=['GET'])
def get_quality_info():
    conn = get_db_connection()
    info = conn.execute('SELECT * FROM quality ORDER BY id DESC').fetchone()
    result = dict(info)
    conn.close()
    return result

@quality.route('/quality', methods=['POST'])
def set_quality_info():
    conn = get_db_connection()
    quality_info = {
        "water_quality": random(),
        "filter_quality": random(),
        "dispenser_quality": random()
    }
    conn.execute("INSERT INTO quality(water_quality,filter_quality,dispenser_quality) VALUES (?, ?, ?)", 
        (quality_info["water_quality"], quality_info['filter_quality'], quality_info['dispenser_quality']))
    conn.commit()
    conn.close()
    return {"message":"Success"}
