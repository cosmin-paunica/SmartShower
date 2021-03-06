from db_conn import get_db_connection
from subprocess import STARTF_USESTDHANDLES
from dispenser import use_dispenser
from flask import Blueprint, request
from quality import set_quality_info
from spotify import get_song
from auth import login_required

from users import get_single_user
from water import add_consumption


shower = Blueprint('shower', __name__)

@shower.route('/start', methods=['GET'])
@login_required
def start_shower():
    # consuma din dispenser
    # pune quality in baza de date
    use_dispenser()
    set_quality_info()
    data = request.get_json(force=True)
    song = get_song(data['song_id'])
    if "error" not in song.keys():
        return {"message":"Shower started successfully!"}
    else:
        return song

@shower.route('/end', methods=['POST'])
@login_required
def end_shower():
    add_consumption()
    return {"message":"Shower ended successfully!"}