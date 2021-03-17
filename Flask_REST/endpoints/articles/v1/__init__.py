from flask import Blueprint
from flask_restful import MethodView

class Articles(MethodView):
	# update imports here to define version
	from Flask_REST.endpoints.articles.common.post import post
	from Flask_REST.endpoints.articles.common.get import get
	from Flask_REST.endpoints.articles.common.put import put
	from Flask_REST.endpoints.articles.common.patch import patch
	from Flask_REST.endpoints.articles.common.delete import delete

article_view = Articles.as_view("articles")
article_endpoint = Blueprint("article_bp", __name__, url_prefix="/v1")
article_endpoint.add_url_rule("/articles/", defaults={"article_id": 0}, view_func=article_view)
article_endpoint.add_url_rule("/articles/<int:article_id>", view_func=article_view)
