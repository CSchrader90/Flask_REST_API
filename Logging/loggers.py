import os
import logging

from instance.config import CHANNEL_LOG_NAME, CHANNEL_LOG_FILE
from instance.config import ARTICLE_LOG_NAME, ARTICLE_LOG_FILE

# Create loggers
channel_logger = logging.getLogger(CHANNEL_LOG_NAME)
article_logger = logging.getLogger(ARTICLE_LOG_NAME)

# Create File Handlers
channel_file_handler = logging.FileHandler(CHANNEL_LOG_FILE)
article_file_handler = logging.FileHandler(ARTICLE_LOG_FILE)

# Set logging formats
formatter = logging.Formatter("%(levelname)s|%(asctime)s|%(message)s")
channel_file_handler.setFormatter(formatter)
article_file_handler.setFormatter(formatter)

# Add Handlers to loggers
channel_logger.addHandler(channel_file_handler)
article_logger.addHandler(article_file_handler)

# Set logging levels based on environment
if os.environ.get("FLASK_ENV") == "production":
    channel_logger.setLevel(logging.INFO)
    article_logger.setLevel(logging.INFO)
elif os.environ.get("FLASK_ENV") == "test":
    channel_logger.setLevel(logging.WARNING)
    article_logger.setLevel(logging.WARNING)
elif os.environ.get("FLASK_ENV") == "development":
    channel_logger.setLevel(logging.DEBUG)
    article_logger.setLevel(logging.DEBUG)
