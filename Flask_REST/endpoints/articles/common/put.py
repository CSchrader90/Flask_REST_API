from flask import request, make_response, jsonify
import requests

from Flask_REST.models.models import ArticleModel, ChannelModel, ArticleSchema, db


def put(self):
	""" Add existing article into existing channel """

	if not request.is_json:
		return make_response("Bad request - JSON body not provided", 400)

	request_args = request.args
	if "article_url" not in request_args:
		return make_response("Valid URL not provided", 400)

	article_url = request_args["article_url"]
	article_exists = ArticleModel.query.filter_by(article_url=article_url).first()
	if not article_exists:
		return make_response("Article at provided URL not found", 404)

	if "channel_name" not in request.get_json():
		return make_response("Channel name not provided", 400)

	new_channel_name = request.get_json()["channel_name"]
	channel = ChannelModel.query.filter_by(channel=new_channel_name).first()
	if not channel:
		channel = ChannelModel(channel=new_channel_name)
		db.session.add(channel)

	if article_exists not in channel.articles:
		channel.articles.append(article_exists)
		db.session.commit()

	return make_response("Article updated", 200)
