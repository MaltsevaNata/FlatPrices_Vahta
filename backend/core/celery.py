import time
from typing import Callable

from celery import Celery
from flask_socketio import emit
from models import RealEstate

from .config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery('celery_worker', broker=CELERY_BROKER_URL)
print("Celery initialized")


@celery.task
def predict_price(data: dict):
    print("predicting price...")
    time.sleep(5)
    print("Finished task")
    emit("price", "300000")



