FROM python:3.9-slim

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip setuptools wheel
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5000
RUN mkdir -p /usr/local/var/log/gunicorn/

CMD ["python", "app.py"]
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "wsgi_app:app"] NOT READY YET