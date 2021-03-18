from flask import make_response, request, jsonify
from werkzeug.security import check_password_hash
import jwt
import datetime

from instance.config import SECRET_KEY, TOKEN_VALID_PERIOD
from Flask_REST.models.models import UserModel

def login():
    verified = False

    auth = request.authorization
    if not auth or not auth.password or not auth.username:
        return make_response("Authorization required (username and password)", 401)

    user_exists = UserModel.query.filter_by(username=auth.username).first()
 
    if user_exists:
        if check_password_hash(user_exists.password, auth.password):
            verified = True
    
    if not verified:
        return make_response("Could not verify user with credentials", 401)

    token = jwt.encode({'public_id' : user_exists.public_id, 
                        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=int(TOKEN_VALID_PERIOD))},
                        SECRET_KEY)
    return jsonify({'token' : token})
