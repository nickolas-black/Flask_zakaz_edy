import os

current_path = os.path.dirname(os.path.realpath(__file__))
db_path = 'sqlite:///' + os.path.join(current_path, 'data.db')



class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "indonesia XENA"