import random
from db_conn import get_db_connection
from subprocess import STARTF_USESTDHANDLES
from flask import Blueprint, request

from users import get_single_user


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
        "water_quality": random.random(),
        "filter_quality": random.random(),
        "dispenser_quality": random.random()
    }
    conn.execute("INSERT INTO quality(water_quality,filter_quality,dispenser_quality) VALUES (?, ?, ?)", 
        (quality_info["water_quality"], quality_info['filter_quality'], quality_info['dispenser_quality']))
    conn.commit()
    conn.close()
    return {"message":"Quality inserted successfully!"}
