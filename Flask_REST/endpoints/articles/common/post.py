from bs4 import BeautifulSoup
from flask import request, make_response, jsonify
from flask_restful import abort
import requests

from Flask_REST.models.models import ArticleModel, ChannelModel, ArticleSchema, db
from Logging.loggers import article_logger

def post(self, article_id):
    """ Add article provided at URL """

    if not request.is_json:
        return make_response("Bad request - no JSON body", 400)
    url = request.get_json()["article_url"]
    article_logger.info(f"Received request to add article|[url: {url}]")

    if not request.is_json or not request.get_json()["article_url"]:
        return make_response("Bad request - URL not provided", 400)

    request_args = request.get_json()
    title, word_count = fetch_url(request_args["article_url"])

    # if article entry at URL exists, fetch again (possible update)
    old_entry = ArticleModel.query.filter_by(article_url=request_args["article_url"]).first()
    if old_entry:
        db.session.delete(old_entry)

    article = ArticleModel(article_url=request_args["article_url"], word_count=word_count, title=title)
    db.session.add(article)
    db.session.commit()

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
