import os


class Config(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'mysql+pymysql://root:wxx1512@localhost:3306/short_url_generation'
    SECRET_KEY = 'you-will-never-guess'
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'
