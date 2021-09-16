from celery import Celery

from .config import CELERY_BROKER_URL

celery = Celery('celery_worker', broker=CELERY_BROKER_URL)
