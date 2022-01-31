import sqlite3
from flask import Flask
import json
from users import users
from dispenser import dispenser
from water import water
app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(dispenser)
app.register_blueprint(water)
