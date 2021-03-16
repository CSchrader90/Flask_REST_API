"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

class BaseConfig:
    JSON_SORT_KEYS = False
    SECRET_KEY = environ.get("SECRET_KEY")

class TestConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_TEST_DATABASE_URI")
    DEBUG=True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DEV_DATABASE_URI")
    DEBUG=True
