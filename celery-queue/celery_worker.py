import os
from celery import Celery
from flask_socketio import SocketIO

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'ampq://rabbitmq:5672'),

celery = Celery('celery_worker', broker=CELERY_BROKER_URL)


@celery.task(name='celery_worker.predict')
def predict_price(data: dict):
    print("predicting price...")
    """
    Здесь вызов функции предсказания цены, передать в нее данные data
    """
    socketIo = SocketIO(message_queue='amqp://rabbitmq:5672')
    """
    и сюда вместо числа 300000 вставить результат - цену
    """
    socketIo.emit("price", "300000")
    print("Finished task")