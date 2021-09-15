import os

from eventlet import monkey_patch as monkey_patch
import eventlet.debug
monkey_patch()

from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

socketIo = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

app.host = 'localhost'
eventlet.debug.hub_prevent_multiple_readers(False)


@socketIo.on('real_estate_data')
def handle_input_data(data):
    print("Got your message")
    emit('my response', {'data': data})


@socketIo.on('connect')
def test_connect(msg):
    print("Connected")
    emit('connect', {'data': 'Connected'})


if __name__ == '__main__':
    socketIo.run(app, host='0.0.0.0', port='5000',
                     debug=True)