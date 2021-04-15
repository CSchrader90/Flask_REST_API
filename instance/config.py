"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

# flask configurations
class BaseConfig:
    JSON_SORT_KEYS = False
    SECRET_KEY = environ.get("SECRET_KEY")
    CACHE_TYPE="SimpleCache" 

class TestConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_PROD_DATABASE_URI")
    DEBUG=True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_PROD_DATABASE_URI")
    CACHE_DEFAULT_TIMEOUT=3

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DEV_DATABASE_URI")
    DEBUG=True
    CACHE_DEFAULT_TIMEOUT=0.0000000001 # Effectively disable cache

# Logging configuration
CHANNEL_LOG_NAME = "channel_log"
ARTICLE_LOG_NAME = "article_log"
CHANNEL_LOG_FILE = "channel.log"
ARTICLE_LOG_FILE = "article.log"

# Security configuration
password = environ.get("PASSWORD")
hash_alg = environ.get("PASSWORD_HASH_ALGORITHM")
salt_len = environ.get("SALT_LENGTH")
SECRET_KEY = environ.get("SECRET_KEY")
TOKEN_VALID_PERIOD = environ.get("TOKEN_VALID_PERIOD")
