import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    SQLALCHEMY_DATABASE_URI = "sqlite:////home/saharsh/Desktop/VJTICrackers/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
