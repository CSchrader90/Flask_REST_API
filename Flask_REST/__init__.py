""" Flask API factory """
from flask import Flask
import os

from .models.models import *
from instance.config import DevelopmentConfig, TestConfig, ProductionConfig
from Flask_REST.endpoints.channels.v1 import channel_endpoint as channel_v1
from Flask_REST.endpoints.articles.v1 import article_endpoint as article_v1

def create_app():
	app = Flask(__name__, instance_relative_config=True)

	# Set the environment variables base on environment
	if(os.environ.get("FLASK_ENV")=="test"):
		app.config.from_object(TestConfig)
	elif(os.environ.get("FLASK_ENV")=="production"):
		app.config.from_object(ProductionConfig)
	else:
		app.config.from_object(DevelopmentConfig)

	db.init_app(app)
	with app.app_context():
		db.create_all()

	app.register_blueprint(channel_v1)
	app.register_blueprint(article_v1)

	return app
