import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'rrr'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://flask_user:yourpassword@localhost/flask_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False