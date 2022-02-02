from flask import (Blueprint, request, jsonify)
from db_conn import get_db_connection
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=["POST"])
def register():
    name = request.form['name']
    password = request.form['password']
    height = request.form['height']
    hair_length = request.form['hair_length']
    db = get_db_connection()

    if not name:
        return jsonify({'status': 'Name is required.'}), 403
    elif not password:
        return jsonify({'status': 'Password is required.'}), 403
    elif not height:
        return jsonify({'status': 'Height is required.'}), 403
    elif not hair_length:
        return jsonify({'status': 'Hair Length is required.'}), 403

    try:
        db.execute(
            "INSERT INTO users (name, password, height, hair_length) VALUES (?, ?, ?, ?)",
            (name, generate_password_hash(password), height, hair_length),
        )
        db.commit()
    except db.IntegrityError:
        return jsonify({'status': f'User {name} is already registered.'}), 403

    return jsonify({'status': 'user registered succesfully'}), 200