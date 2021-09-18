import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO, emit

import joblib
import pandas as pd

import json
import traceback

from core import config
from models import RealEstate
from utils import validate
from core.celery import celery
from core.enrichers import enrich_data
from core.fields_to_numbers import fields_to_numbers


class WebSocketAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = config.SECRET_KEY

        self.socketIo = SocketIO(self.app, async_mode='eventlet', cors_allowed_origins="*",
                                 message_queue=f'amqp://{config.RABBIT_HOST}:{config.RABBIT_PORT}')
        self.socketIo.on_event('connect', self.connect, namespace='/')
        self.socketIo.on_event('real_estate_data', self.handle_input_data, namespace='/')
        with open('./predict_models/moscow_model.pkl', 'rb') as f:
            self.moscow_model = joblib.load(f)
        with open('./predict_models/saintp_model.pkl', 'rb') as f:
            self.saintp_model = joblib.load(f)

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
        if isinstance(data, str):
            data = json.loads(data)
        emit('got_data', {'data': data.dict()})
        try:
            enriched_data = enrich_data(data)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            self.on_error("Failed to parse address, please check format")
        else:
            modified_data_dict = fields_to_numbers(enriched_data)
            #self.socketIo.start_background_task(celery.send_task, 'celery_worker.predict', [modified_data_dict])
            self.socketIo.start_background_task(self.background_task, modified_data_dict)

    def background_task(self, data: dict):
        """
        THIS IS A TEMPORARY SOLUTION INSTEAD OF CELERY TASKS, CAN BE USED ONLY FOR 1 CLIENT
        """

        print("predicting price...")

        df = pd.DataFrame(data)
        features = [
            'total_area',
            'living_area',
            'kitchen_area',
            'floor_number',
            'total_floors',
            'year',
            'material_type',
            'underground',
            'distance',
            'azimuth'
        ]
        val_X = df[features]

        if df['region'][0] == 1:
            price = self.moscow_model.predict(val_X)[0]
        else:
            price = self.saintp_model.predict(val_X)[0]
        print(f"Price was predicted: {price}")

        aqi = {1: "Высокое", 2: "Высокое", 3: "Среднее", 4: "Низкое", 5: "Низкое"}
        air_quality = aqi[data["AQI"]]

        self.socketIo.emit("price",
                      {"price": round(price, 0), "refund": round((price - 0.1 * price), 0), "air_quality": air_quality,
                       "components": {"co": round(data["air_pollutant_concentration"]["co"] / 1000, 2)}},
                      broadcast=True)
        print("Finished task")




