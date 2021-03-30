from flask import request, make_response, jsonify
import requests

from Flask_REST.models.models import ArticleModel, ChannelModel, ArticleSchema, db
from Logging.loggers import article_logger
from Flask_REST.authorization.auth import verify_token
from Flask_REST.endpoints.request_checks.checkForJsonBody import verify_json

@verify_token
@verify_json(logger=article_logger, verb="PATCH", required_field="channel_name")
def patch(self, user, article_id):
	""" Remove an article from a channel"""

	if article_id == 0:
		article_logger.error(f"Article not found (article_id not provided to PUT) [url: {article.article_url}]")
		return make_response("Bad request - article_id not provided", 400)

	article = ArticleModel.query.filter_by(user=user.username, article_id=article_id).first()
	if not article:
		article_logger.error(f"Article not found with given article_id to PUT [url: {article.article_url}]")
		return make_response("Article not found", 404)

	request_body = request.get_json()
	channel = ChannelModel.query.filter_by(user=user.username, 
										   channel=request_body["channel_name"]).first()
	if not channel:
		article_logger.error(f"Channel not found with given channel to PUT [channel: {request_body['channel_name']}]")
		return make_response("Channel not found", 404)

	channel.articles.remove(article)
	db.session.commit()
	article_logger.info(f"Article removed from channel - PUT [url: {article.article_url}]")
	return make_response("Article removed from channel", 200)
