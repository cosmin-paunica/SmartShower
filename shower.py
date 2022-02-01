import sqlite3
from subprocess import STARTF_USESTDHANDLES
from dispenser import use_dispenser
from flask import Blueprint, request
from quality import set_quality_info

from users import get_single_user
from water_consumption import add_consumption

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

shower = Blueprint('shower', __name__)

@shower.route('/start', methods=['GET'])
def start_shower():
    # consuma din dispenser
    # pune quality in baza de date
    use_dispenser()
    set_quality_info()
    return {"message":"Shower started successfully!"}

@shower.route('/end', methods=['POST'])
def end_shower():
    add_consumption()
    return {"message":"Shower ended successfully!"}