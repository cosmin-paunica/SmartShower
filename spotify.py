
from dotenv import load_dotenv
import os

from db_conn import get_db_connection
from subprocess import STARTF_USESTDHANDLES
from flask import Blueprint
import requests


load_dotenv()
SECRET_KEY = os.getenv("SPOTIFY_TOKEN")

spotify = Blueprint('spotify', __name__)

@spotify.route('/song/<songid>', methods=['GET'])
def get_song(songid):
    song = requests \
        .get(f'https://api.spotify.com/v1/tracks/{songid}',
                headers={'Authorization': f'Bearer {SECRET_KEY}'}) \
        .json()

    return song