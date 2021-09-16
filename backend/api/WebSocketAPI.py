from flask import Flask
from flask_socketio import SocketIO, emit

from core import config
from models import RealEstate
from utils import validate
from core.celery import celery
from core.eco_enricher import eco_enrich


class WebSocketAPI:
    def __init__(self):
        self.app = Flask(__name__)
        print(__name__)
        self.app.config['SECRET_KEY'] = config.SECRET_KEY
        self.socketIo = SocketIO(self.app, async_mode='eventlet', cors_allowed_origins="*", message_queue='amqp://rabbitmq:5672')
        import eventlet
        eventlet.monkey_patch()
        self.socketIo.on_event('connect', self.connect, namespace='/')
        self.socketIo.on_event('real_estate_data', self.handle_input_data, namespace='/')

    def run(self):
        self.socketIo.run(self.app, host=config.HOST, port=config.PORT, debug=True)

    def on_error(self, msg: str):
        print(msg)
        emit("error", msg)

    def connect(self):
        print("Connected")
        emit('connect', {'data': 'Connected'})

    @validate(cls=RealEstate, err_callback=on_error)
    def handle_input_data(self, data: RealEstate):
        print("Got your message")
        emit('got_data', {'data': data.dict()})
        enriched_data = eco_enrich(data)
        self.socketIo.start_background_task(celery.send_task, 'celery_worker.predict', [enriched_data.dict()])







