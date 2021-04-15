from flask import request, make_response, jsonify

from Flask_REST.caching.caching import cache, cache_key
from Flask_REST.models.models import ArticleModel, ChannelModel, ArticleSchema, db
from Logging.loggers import article_logger
from Flask_REST.authorization.auth import verify_token

@verify_token
@cache.cached()
def get(self, user, article_id):
	""" Get single article provided in URI or list all """
	
	if article_id == 0: # no article id provided - return all articles
		article_objects = ArticleModel.query.filter_by(user=user.username).all()
		schema = ArticleSchema(many=True)
		output = schema.dump(article_objects)
		return make_response(jsonify(output), 200)

	article = ArticleModel.query.filter_by(user=user.username, article_id=article_id).first()
	if article is None:
		article_logger.error(f"Article not found [article_id: {article_id}]")
		return make_response("Article not found", 404)

	article_logger.info(f"Article found [url: {article.article_url}]")
	schema = ArticleSchema(many=False)
	output = schema.dump(article)
	article_logger.info(f"Returning article [url: {article.article_url}]")
	return make_response(output, 200)
