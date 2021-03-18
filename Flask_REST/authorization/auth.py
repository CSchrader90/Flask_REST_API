from flask import request, make_response
import jwt
from functools import wraps

from instance.config import SECRET_KEY
from Flask_REST.models.models import UserModel

def verify_token(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response("access token not found", 401)

#        try: 
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(data['public_id'])
        user = UserModel.query.filter_by(public_id=data['public_id']).first()
#        except:
#           return make_response("invalid token", 401)

        return f(self, user, *args, **kwargs)

    return decorated