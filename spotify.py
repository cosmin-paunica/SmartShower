
from dotenv import load_dotenv
import os

from db_conn import get_db_connection
from subprocess import STARTF_USESTDHANDLES
from flask import Blueprint
import requests


load_dotenv()
SECRET_KEY = os.getenv("SPOTIFY_TOKEN")

spotify = Blueprint('spotify', __name__)

@spotify.route('/song/<id>', methods=['GET'])
def get_song(id):
    song = requests.get(f'https://api.spotify.com/v1/tracks/{id}').json()
    return song