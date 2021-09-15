import os

SECRET_KEY = os.environ.get("SECRET_KEY")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", "5000")