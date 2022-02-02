import eventlet
import json
import auth
import time

from flask import Flask
from threading import Thread
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

from users import users
from dispenser import dispenser
from water import water
from quality import quality
from shower import shower
from status import get_status
from spotify import spotify

eventlet.monkey_patch()


app = None
mqtt = None
socketio = None
thread = None


def create_app():
    global app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'PDS19UkUAd1H1NiAqJjGAFT6KrN78W5J'

    app.register_blueprint(auth.bp)
    app.register_blueprint(users)
    app.register_blueprint(dispenser)
    app.register_blueprint(water)
    app.register_blueprint(quality)
    app.register_blueprint(shower)
    app.register_blueprint(spotify)

    @app.route('/')
    def welcome():
        global thread
        if thread is None:
            thread = Thread(target=background_thread)
            thread.daemon = True
            thread.start()
        return 'Welcome to SmartShower!'

    return app


def create_mqtt_app():
    # Setup connection to mqtt broker
    app.config['MQTT_BROKER_URL'] = '127.0.0.1'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    global mqtt
    mqtt = Mqtt(app)
    global socketio 
    socketio = SocketIO(app, async_mode="eventlet")

    return mqtt

# Start MQTT publishing
# Function that every second publishes a message
def background_thread():
    count = 0
    while True:
        time.sleep(1)
        # Using app context is required because the get_status() functions
        # requires access to the db.
        with app.app_context():
            message = json.dumps(get_status(), default=str)
        # Publish
        mqtt.publish('python/mqtt', message)

# App will now have to be run with `python app.py` as flask is now wrapped in socketio.
# The following makes sure that socketio is also used

def run_socketio_app():
    create_app()
    # create_mqtt_app()
    socketio.run(app, host='127.0.0.1', port=5000, use_reloader=False, debug=True)

if __name__ == '__main__':
    run_socketio_app()