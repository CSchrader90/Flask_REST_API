from flask import request, make_response, jsonify
import requests

from Flask_REST.models.models import ArticleModel, ChannelModel, ArticleSchema, db
from Logging.loggers import article_logger

def delete(self, article_id):
	"""Delete provided article"""

	if article_id == 0:
		return make_response("article_id not provided", 400)

	article_exists = ArticleModel.query.filter_by(article_id=article_id).first()
	if not article_exists:
		return make_response("Article at provided article id not found", 404)

	delete_article = ArticleModel.query.filter_by(article_id=article_id).first()
	db.session.delete(delete_article)
	db.session.commit()

	return make_response("Article Deleted", 200)
