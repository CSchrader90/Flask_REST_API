from flask import request, make_response, jsonify
import requests

from Flask_REST.models.models import ArticleModel, ChannelModel, ArticleSchema, db

def patch(self):
	""" Remove an article from a channel"""
	if not request.is_json:
		return make_response("Bad request - JSON body not provided", 400)

	if "article_url" not in request.args:
		return make_response("Valid URL not provided", 400)

	request_body = request.get_json()

	if "channel_name" not in request_body:
		return make_response("Channel name not provided", 400)

	article = ArticleModel.query.filter_by(article_url=request.args["article_url"]).first()
	if not article:
		return make_response("Article not found", 404)

	channel = ChannelModel.query.filter_by(channel=request_body["channel_name"]).first()
	if not channel:
		return make_response("Channel not found", 404)

	channel.articles.remove(article)
	db.session.commit()
	return make_response("Article removed from channel", 200)

