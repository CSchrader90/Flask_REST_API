from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash
import datetime
import uuid
import jwt

from Flask_REST.models.models import db, UserModel
from instance.config import salt_len, SECRET_KEY, TOKEN_VALID_PERIOD

def create_user():

    username = request.get_json()["username"]
    password = request.get_json()["password"]

    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']

    if not token:
        return make_response("access token not found", 401)
    try: 
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        root_user = UserModel.query.filter_by(public_id=data['public_id']).first()
    except:
        return make_response("invalid token", 401)

    if not root_user or not root_user.is_root:
        return make_response("Only root user can create other users", 401)

    user_exists = UserModel.query.filter_by(username=username).first()
    if user_exists:
        return make_response("User name already taken", 400)

    new_user = UserModel(username=username, \
                        password = generate_password_hash(password, salt_length=int(salt_len)),
                        public_id = str(uuid.uuid4()),
                        is_root = False)

    db.session.add(new_user)
    db.session.commit()

    return make_response("New user created", 201)