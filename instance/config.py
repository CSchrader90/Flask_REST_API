"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

# flask configurations
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

# Logging configuration
CHANNEL_LOG_NAME = "channel_log"
ARTICLE_LOG_NAME = "article_log"
CHANNEL_LOG_FILE = "Logging/channel.log"
ARTICLE_LOG_FILE = "Logging/article.log"
