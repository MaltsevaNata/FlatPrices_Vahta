import os
from celery import Celery
from flask_socketio import SocketIO

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://rabbitmq:5672'),

celery = Celery('celery_worker', broker=CELERY_BROKER_URL)


@celery.task(name='celery_worker.predict')
def predict_price(data: dict):
    print("predicting price...")
    """
    Здесь вызов функции предсказания цены, передать в нее данные data
    """
    socketIo = SocketIO(message_queue='amqp://rabbitmq:5672')
    """
    и сюда вместо числа 10000 вставить результат - цену, а в refund вставить цену -10%
    """

    socketIo.emit("price", {"price": 10000, "refund": 9500, "air_quality": data["AQI"],
                            "components": {"co": data["air_pollutant_concentration"]["co"]}})
    print("Finished task")