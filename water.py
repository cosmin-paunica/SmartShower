import sqlite3
from subprocess import STARTF_USESTDHANDLES
from flask import Blueprint, request

from users import get_single_user

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

water = Blueprint('water', __name__)
