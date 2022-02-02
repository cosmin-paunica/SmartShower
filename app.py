import sqlite3
from venv import create
from flask import Flask
import json
from users import users
from dispenser import dispenser
from water import water
from quality import quality
from water_consumption import water_consumption
from shower import shower
import auth

app = None

def create_app():
    global app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'PDS19UkUAd1H1NiAqJjGAFT6KrN78W5J'

    app.register_blueprint(auth.bp)
    app.register_blueprint(users)
    app.register_blueprint(dispenser)
    app.register_blueprint(water)
    app.register_blueprint(quality)
    app.register_blueprint(water_consumption)
    app.register_blueprint(shower)

    @app.route('/')
    def welcome():
        return 'Welcome to SmartShower!'

    return app


def run_socketio_app():
    create_app()


if __name__ == '__main__':
    run_socketio_app()