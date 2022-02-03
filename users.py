import sqlite3
from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

users = Blueprint('users', __name__)

#Get all users
@users.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    user_rows = conn.execute('SELECT name, height, hair_length FROM users')
    result = []
    for row in user_rows:
        result.append(dict(row))
    conn.close()
    return {"users": result}

@users.route('/users', methods=['POST'])
def add_user():
    conn = get_db_connection()
    data = request.get_json(force=True)

    try:
        name = data['name']
        height = data['height']
        hair_length = data['hair_length']
        password = data['password']
    except:
        conn.close()
        return {'message' : 'Fields must be nonempty!'}


    conn.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (name, generate_password_hash(password), height, hair_length))
    conn.commit()
    conn.close()

    return data

@users.route('/users/<name>', methods=['GET'])
def get_single_user(name):
    conn = get_db_connection()
    user_rows= conn.execute('SELECT name, height, hair_length FROM users WHERE name = (?)', (name,)).fetchall()

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
    return {'message' : 'User updated!'}

@users.route('/users/<name>', methods=['DELETE'])
def delete_user(name):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE name = ?', (name,))
    conn.commit()
    return {'message':'Successfully deleted!'}
