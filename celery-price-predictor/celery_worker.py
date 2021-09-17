import os
from celery import Celery
from flask_socketio import SocketIO

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://rabbitmq:5672'),

celery = Celery('celery_worker', broker=CELERY_BROKER_URL)

with open('./moscow_model.pkl', 'wb') as f:
    moscow_model = joblib.load(f)

with open('./saintp_model.pkl', 'wb') as f:
    saintp_model = joblib.load(f)

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

    if df['region'] == 'Moscow':
        price = moscow_model.predict(val_X)
        if price < 4000000:
            price = 4100000
    else:
        price = saintp_model.predict(val_X)
        if price < 260000:
            price = 2650000

    socketIo = SocketIO(message_queue='amqp://rabbitmq:5672')

    socketIo.emit("price", {"price": price, "refund": (price - 0.1 * price), "air_quality": data["AQI"],
                            "components": {"co": data["air_pollutant_concentration"]["co"]}})
    print("Finished task")