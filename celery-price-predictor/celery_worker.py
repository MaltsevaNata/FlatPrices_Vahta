import eventlet
eventlet.monkey_patch()
import os

from celery import Celery
from flask_socketio import SocketIO
import joblib
import pandas as pd

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://rabbitmq:5672'),

celery = Celery('celery_worker', broker=CELERY_BROKER_URL)


@celery.task(name='celery_worker.predict')
def predict_price(data: dict):
    """
    :param data: {'region': 2, 'material_type': 1, 'total_area': 18.0, 'living_area': 15.0, 'kitchen_area': 3.0,
    'floor_number': 12, 'total_floors': 15, 'year': 2005, 'address': 'Begovaya, 25',
    'underground': 1, 'lat': 59.988275, 'lon': 30.205824, 'AQI': 1, 'air_pollutant_concentration':
    {'co': 494, 'no': 1.76, 'no2': 39.41, 'o3': 10.01, 'so2': 27.18, 'pm2_5': 2.47, 'pm10': 3.42, 'nh3': 0.49},
     'azimuth': 314.67, 'distance': 8059.998925556098}
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
        with open('./moscow_model.pkl', 'rb') as f:
            moscow_model = joblib.load(f)
        price = moscow_model.predict(val_X)[0]
    else:
        with open('./saintp_model.pkl', 'rb') as f:
            saintp_model = joblib.load(f)
        price = saintp_model.predict(val_X)[0]
    print(f"Price was predicted: {price}")
    socketIo = SocketIO(message_queue='amqp://rabbitmq:5672', )

    aqi = {1: "Высокое", 2: "Высокое", 3: "Среднее", 4: "Низкое", 5: "Низкое"}
    air_quality = aqi[data["AQI"]]

    socketIo.emit("price", {"price": round(price,0), "refund": round((price - 0.1 * price),0), "air_quality": air_quality,
                            "components": {"co": round(data["air_pollutant_concentration"]["co"]/1000, 2)}}, broadcast=True)
    print("Finished task")