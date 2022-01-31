import sqlite3
from flask import Blueprint, request

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

users = Blueprint('users', __name__)

#Get all users
@users.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    user_rows = conn.execute('SELECT * FROM users')
    result = []
    for row in user_rows:
        result.append(dict(row))
    conn.close()
    return {"users": result}

@users.route('/users', methods=['POST'])
def add_user():
    conn = get_db_connection()
    data = request.get_json(force=True)
    name = data['name']
    height = data['height']
    hair_length = data['hair_length'] 
    #TODO: check parameter validity for the above fields
    # I think ??? or should we assume they are correct ?

    conn.execute('INSERT INTO users VALUES (?, ?, ?)', (name, height, hair_length))
    conn.commit()
    conn.close()

    return data

@users.route('/users/<name>', methods=['GET'])
def get_single_user(name):
    conn = get_db_connection()
    user_rows= conn.execute('SELECT * FROM users WHERE name = (?)', (name,)).fetchall()

    result = {}
    for row in user_rows:
        result = dict(row)  #should only execute once

    conn.close()
    return result

@users.route('/users/<name>', methods=['PUT'])
def modify_user(name):
    conn = get_db_connection()
    data = request.get_json(force=True)
    new_name = data['new_name']
    new_height = data['new_height']
    new_hair_length = data['new_hair_length']
    conn.execute('UPDATE users SET name = ?, height = ?, hair_length = ? WHERE name = ?', (new_name, new_height, new_hair_length, name))
    conn.commit()
    conn.close()
    return data

@users.route('/users/<name>', methods=['DELETE'])
def delete_user(name):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE name = ?', (name,))
    conn.commit()
    return {'meesage':'successfully deleted'}
