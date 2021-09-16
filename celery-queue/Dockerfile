FROM python:3.9-slim

ENV CELERY_BROKER_URL amqp://rabbitmq:5672
ENV C_FORCE_ROOT true

COPY . /queue
WORKDIR /queue

RUN pip install -r requirements.txt

# production
ENTRYPOINT celery -A celery_worker worker --loglevel=info