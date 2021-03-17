from flask import request, make_response, jsonify
import requests

from Flask_REST.models.models import ArticleModel, ChannelModel, ArticleSchema, db
from Logging.loggers import article_logger


def get(self, article_id):
	""" Get single article provided in URI or list all """
	
	if article_id == 0: # no article id provided - return all articles
		article_objects = ArticleModel.query.all()
		schema = ArticleSchema(many=True)
		output = schema.dump(article_objects)
		return make_response(jsonify(output), 200)

	article = ArticleModel.query.filter_by(article_id=article_id).first()
	if not article:
		return make_response("Article not found", 404)

	schema = ArticleSchema(many=False)
	output = schema.dump(article)
	return make_response(output, 200)
