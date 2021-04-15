from flask import request, make_response
import json
from functools import wraps


def verify_json(logger, verb, required_field):
    def middle_func(func):
        @wraps(func)
        def decorated(self, *args, **kwargs):

            if not request.is_json:
                logger.error(f"Failed (JSON body not found)|[verb:{verb}]")
                return make_response("Bad request - no JSON body", 400)

            json_body = request.get_json()

            if required_field not in json_body:
                logger.error(f"JSON field not found|[verb:{verb},required_field:{required_field}]")
                return make_response(f"required JSON field \"{required_field}\" not found ", 400)

            return func(self, *args, **kwargs)

        return decorated
        
    return middle_func
