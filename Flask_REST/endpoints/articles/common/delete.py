from flask import request, make_response, jsonify
import requests

from Flask_REST.models.models import ArticleModel, ChannelModel, ArticleSchema, db
from Logging.loggers import article_logger
from Flask_REST.authorization.auth import verify_token

@verify_token
def delete(self, user, article_id):
	"""Delete provided article"""

	if article_id == 0:
		article_logger.error(f"article_id not provided to delete [article_id: <none>])
		return make_response("article_id not provided", 400)

	article_exists = ArticleModel.query.filter_by(user=user.username,
												  article_id=article_id).first()
	if not article_exists:
		article_logger.error(f"Article not found at given article_url for delete [article_id: {article_id}])
		return make_response("Article at provided article id not found", 404)

	delete_article = ArticleModel.query.filter_by(user=user.username, 
												article_id=article_id).first()
	db.session.delete(delete_article)
	db.session.commit()

	article_logger.info(f"Article delete [article_id: {article_id}]")
	return make_response("Article Deleted", 200)
