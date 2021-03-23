""" Flask API factory """
from flask import Flask
import os
import uuid
from werkzeug.security import generate_password_hash

from .models.models import db, UserModel
from instance.config import DevelopmentConfig, TestConfig, ProductionConfig
from instance.config import password, hash_alg, salt_len
from .endpoints.channels.v1 import channel_endpoint as channel_v1
from .endpoints.articles.v1 import article_endpoint as article_v1
from .endpoints.login import login_v1
from .endpoints.users import users_v1

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

		# create a new root user if doesn't exist
		root_user_exists = UserModel.query.filter_by(is_root=True).first()
		if not root_user_exists:
			db.session.add(UserModel(username="root", \
									password = generate_password_hash(password, salt_length=int(salt_len)),
									public_id = str(uuid.uuid4()),
									is_root = True))
			db.session.commit()

	app.register_blueprint(channel_v1)
	app.register_blueprint(article_v1)
	app.add_url_rule("/login/", "login", login_v1.login, methods=["POST"])
	app.add_url_rule("/user/", "user", users_v1.create_user, methods=["POST"])

	return app
