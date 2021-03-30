from flask import request, make_response, jsonify
import requests

from Flask_REST.models.models import ArticleModel, ChannelModel, ArticleSchema, db
from Logging.loggers import article_logger
from Flask_REST.authorization.auth import verify_token

@verify_token
def put(self, user, article_id):
	""" Add existing article into existing channel """

	if article_id == 0:
		article_logger.error(f"Failed to find article_id in PUT|[article_id:<none>]")
		return make_response("Bad request - article id not provided", 400)

	if not request.is_json:
		article_logger.error(f"Failed find JSON body in PUT|[article_id:<none>]")
		return make_response("Bad request - JSON body not provided", 400)

	if "channel_name" not in request.get_json():
		article_logger.error(f"Failed to find channel in PUT|[channel: <none>, article_id: {article_id}]")
		return make_response("Channel name not provided", 400)

	article_exists = ArticleModel.query.filter_by(user=user.username, 
												  article_id=article_id).first()
	if not article_exists:
		article_logger.error(f"Article not found in PUT|[article_id:{article_id}]")
		return make_response("Article with provided id not found", 404)

	new_channel_name = request.get_json()["channel_name"]
	channel = ChannelModel.query.filter_by(user=user.username, 
											channel=new_channel_name).first()
	if not channel: # if channel doesn't exist, create it
		article_logger.info(f"channel not found in PUT - creating|[article_id:{article_id},channel:{new_channel_name}]")
		channel = ChannelModel(user=user.username, channel=new_channel_name)
		db.session.add(channel)

	if article_exists not in channel.articles:
		channel.articles.append(article_exists)
		db.session.commit()

	article_logger.info(f"Article updated with channel in PUT|[article_id:{article_id}, channel:{new_channel_name}]")
	return make_response("Article updated", 200)
