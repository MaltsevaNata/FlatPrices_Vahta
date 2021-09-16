import os

SECRET_KEY = os.environ.get("SECRET_KEY")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", "5000")

RABBIT_HOST = os.environ.get("RABBIT_HOST", "localhost")
RABBIT_PORT = os.environ.get("RABBIT_PORT", "5672")
CELERY_BROKER_URL = 'amqp://' + RABBIT_HOST + ':' + RABBIT_PORT
CELERY_RESULT_BACKEND = 'amqp://' + RABBIT_HOST + ':' + RABBIT_PORT

DADATA_TOKEN = os.environ.get("DADATA_TOKEN", "b3afb646c673637743008c358d7eba1db20a1308")
DADATA_URL = os.environ.get("DADATA_URL", "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address")

OWM_TOKEN = os.environ.get("OWM_TOKEN", "ac5a31dc0a68eb9b7ffa6b2f72999c40")
OWM_URL = os.environ.get("OWM_URL", "http://api.openweathermap.org/data/2.5/")