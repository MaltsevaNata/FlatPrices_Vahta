import os

from celery import Celery
from flask_socketio import SocketIO
import joblib
import pandas as pd

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://rabbitmq:5672'),

celery = Celery('celery_worker', broker=CELERY_BROKER_URL)



@celery.task(name='celery_worker.predict')
def predict_price(data: dict):
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
        with open('./moscow_model.pkl', 'rb') as f:
            moscow_model = joblib.load(f)
        price = moscow_model.predict(val_X)[0]
    else:
        with open('./saintp_model.pkl', 'rb') as f:
            saintp_model = joblib.load(f)
        price = saintp_model.predict(val_X)[0]
    print(price)
    socketIo = SocketIO(message_queue='amqp://rabbitmq:5672')

    socketIo.emit("price", {"price": price, "refund": (price - 0.1 * price), "air_quality": data["AQI"],
                            "components": {"co": round(data["air_pollutant_concentration"]["co"]/1000, 2)}}, broadcast=True)
    print("Finished task")