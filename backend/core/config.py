import os

SECRET_KEY = os.environ.get("SECRET_KEY")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", "5000")

RABBIT_HOST = "rabbitmq"
RABBIT_PORT = "5672"
CELERY_BROKER_URL = 'amqp://' + RABBIT_HOST + ':' + RABBIT_PORT
CELERY_RESULT_BACKEND = 'rpc://'