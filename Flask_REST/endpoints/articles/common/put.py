from flask import request, make_response, jsonify
import requests

from Flask_REST.models.models import ArticleModel, ChannelModel, ArticleSchema, db
from Logging.loggers import article_logger


def put(self, article_id):
	""" Add existing article into existing channel """

	if article_id == 0:
		return make_response("Bad request - article id not provided", 400)

	if not request.is_json:
		return make_response("Bad request - JSON body not provided", 400)

	if "channel_name" not in request.get_json():
		return make_response("Channel name not provided", 400)

	article_exists = ArticleModel.query.filter_by(article_id=article_id).first()
	if not article_exists:
		return make_response("Article with provided id not found", 404)

	new_channel_name = request.get_json()["channel_name"]
	channel = ChannelModel.query.filter_by(channel=new_channel_name).first()
	if not channel: # if channel doesn't exist, create it
		channel = ChannelModel(channel=new_channel_name)
		db.session.add(channel)

	if article_exists not in channel.articles:
		channel.articles.append(article_exists)
		db.session.commit()

	return make_response("Article updated", 200)
