from bs4 import BeautifulSoup
from flask import request, make_response, jsonify
from flask_restful import abort
import requests

from Flask_REST.caching.caching import cache, cache_key
from Flask_REST.models.models import ArticleModel, ChannelModel, ArticleSchema, db
from Logging.loggers import article_logger
from Flask_REST.authorization.auth import verify_token

@verify_token
@cache.cached(key_prefix=cache_key)
def post(self, user, article_id):
    """ Add article provided at URL """

    if not request.is_json:
        article_logger.error(f"Failed to add article (JSON not found in POST)|[url:<none>]")
        return make_response("Bad request - no JSON body", 400)
    url = request.get_json()["article_url"]
    article_logger.info(f"Received request to add article|[url: {url}]")

    if not request.is_json or not request.get_json()["article_url"]:
        article_logger.error(f"Failed to add article (URL not provided in POST)|[url:<none>]")
        return make_response("Bad request - URL not provided", 400)

    request_args = request.get_json()
    title, word_count = fetch_url(request_args["article_url"])
    article_logger.info(f"Fetched article|[url: {url}")

    # if article entry at URL exists, fetch again (possible update)
    old_entry = ArticleModel.query.filter_by(user=user.username, article_url=request_args["article_url"]).first()
    if old_entry:
        article_logger.debug(f"Added article found in database - refetching|[url:{url}]")
        db.session.delete(old_entry)

    article = ArticleModel(user=user.username, article_url=request_args["article_url"], 
                           word_count=word_count, title=title)
    db.session.add(article)
    db.session.commit()

    article_logger.info(f"Added article to database|[url:{url}]")
    return make_response("Article Entered", 201)

def fetch_url(url):
    try:
        html_source = requests.get(url)
    except requests.exceptions.MissingSchema:
        abort(400, message="Please provide valid url with prefixed protocol e.g. https://")
    except requests.exceptions.ConnectionError:
        abort(404, message="Could not fetch provided URL")

    # naive solution to count words in article
    soup = BeautifulSoup(html_source.text, 'lxml')
    title = soup.find('title').text
    paragraphs = soup.find_all('p')
    word_count = 0

    for par in paragraphs:
        word_count += len(par.text.split())

    return title, word_count
