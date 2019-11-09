import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_secret_key'

class Development(Config):
    ENV="dev"
    DEBUG = True
    SECRET_KEY = Config.SECRET_KEY
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

class Testing(Config):
    ENV="testing"
    TESTING = True
    SECRET_KEY = Config.SECRET_KEY
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///app_test.db"

class Production(Config):
    pass


config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}
