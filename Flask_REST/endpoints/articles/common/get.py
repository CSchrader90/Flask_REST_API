from flask import request, make_response, jsonify
import requests

from Flask_REST.models.models import ArticleModel, ChannelModel, ArticleSchema, db


def get(self):
	""" Get single article provided in URI or list all """

	if "article_url" not in request.args:
		article_objects = ArticleModel.query.all()
		schema = ArticleSchema(many=True)
		output = schema.dump(article_objects)
		return make_response(jsonify(output), 200)

	article_url = request.args["article_url"]
	article = ArticleModel.query.filter_by(article_url=article_url).first()
	if not article:
		return make_response("Article not found", 404)

	schema = ArticleSchema(many=False)
	output = schema.dump(article)
	return make_response(output, 200)
