import functools
from flask import (Blueprint, request, jsonify, session, g)
from db_conn import get_db_connection
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=["POST"])
def register():
    '''
    name = request.form['name']
    password = request.form['password']
    height = request.form['height']
    hair_length = request.form['hair_length']
    '''
    db = get_db_connection()
    data = request.get_json(force=True)
    try:
        name = data['name']
    except KeyError:
        return jsonify({'message': 'Name is required.'}), 403

    try:
        password = data['password']
    except KeyError:
        return jsonify({'message': 'Password is required.'}), 403
    
    try:
        height = data['height']
    except KeyError:
        return jsonify({'message': 'Height is required.'}), 403

    try:    
        hair_length = data['hair_length']
    except KeyError:
        return jsonify({'message': 'Hair Length is required.'}), 403


    try:
        db.execute(
            "INSERT INTO users (name, password, height, hair_length) VALUES (?, ?, ?, ?)",
            (name, generate_password_hash(password), height, hair_length),
        )
        db.commit()
    except db.IntegrityError:
        return jsonify({'message': f'User {name} is already registered.'}), 403

    return jsonify({'message': 'user registered succesfully'}), 200

@bp.route('/login', methods=["POST"])
def login():
    print("Hit")
    db = get_db_connection()
    data = request.get_json(force=True)
    name = data['name']
    password = data['password']
    error = None
    user = db.execute(
        'SELECT * FROM users WHERE name = ?', (name,)
    ).fetchone()

    if user is None:
        return jsonify({'message': 'user not found'}), 403
    elif not check_password_hash(user['password'], password):
        return jsonify({'message': 'password is incorrect'}), 403

    session.clear()
    session['user_id'] = user['name']
    return jsonify({'message': 'user logged in succesfully'}), 200

@bp.route('/logout')
def logout():
    session.clear()
    return jsonify({'message': 'user logged out succesfully'}), 200


# !!!!NETESTATE!!!! (they should work tho)
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({'message': 'User is not authenticated'}), 403
        return view(**kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db_connection().execute(
            'SELECT * FROM users WHERE name = ?', (user_id,)
        ).fetchone()