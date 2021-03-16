from flask import request, make_response, jsonify
import requests

from Flask_REST.models.models import ArticleModel, ChannelModel, ArticleSchema, db

def delete(self):
	"""Delete provided article"""

	if "article_url" not in request.args:
		return make_response("Valid URL not provided", 400)
	article_url = request.args["article_url"]
	article_exists = ArticleModel.query.filter_by(article_url=article_url).first()
	if not article_exists:
		return make_response("Article at provided URL not found", 404)

	delete_article = ArticleModel.query.filter_by(article_url=article_url).first()
	db.session.delete(delete_article)
	db.session.commit()

	return make_response("Article Deleted", 200)

