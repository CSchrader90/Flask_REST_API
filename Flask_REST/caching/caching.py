from flask import request
from flask_caching import Cache

cache = Cache()

def cache_key():
    return hash(str(request.get_json()))
