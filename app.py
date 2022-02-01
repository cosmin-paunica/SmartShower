import sqlite3
from flask import Flask
import json
from users import users
from dispenser import dispenser
from water import water
from quality import quality
from water_consumption import water_consumption
from shower import shower
app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(dispenser)
app.register_blueprint(water)
app.register_blueprint(quality)
app.register_blueprint(water_consumption)
app.register_blueprint(shower)