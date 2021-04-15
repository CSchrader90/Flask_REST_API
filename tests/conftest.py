import os
import pytest
from Flask_REST.models.models import db, UserModel, ArticleModel, ChannelModel
import jwt
import datetime
import json
from werkzeug.security import generate_password_hash
from instance.config import SECRET_KEY, salt_len

TEST_DATABASE="../database/test_database.db"
SQLALCHEMY_TEST_DATABASE_URI="sqlite:///"+TEST_DATABASE
MAX_TEST_LENGTH = 1 # max minutes set for all the tests in a module (used for token validity period)
ERRONEOUS_KEY = "SCERET"

TEST_URL="https://www.visitfinland.com/"
TEST_REQUIRED_FIELD = "article_url"

TEST_USER = UserModel(
        username = "root",
        password = generate_password_hash("admin_password", salt_length=int(salt_len)),
        private_id  = 1,
        public_id = "public_id",
        is_root  = True    
        )

@pytest.fixture(scope="module")
def app_fixture(request):
    """ Create flask app """
    from Flask_REST import create_app
    app = create_app()
    
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_TEST_DATABASE_URI
    )
    return app

@pytest.fixture(scope="module")
def app_context_fixture(app_fixture):
    """Create flask app context"""
    with app_fixture.app_context():
        db.create_all()
        db.session.add(TEST_USER)
        db.session.commit()
        yield app_fixture

        db.session.remove()
        db.drop_all()
        os.remove(TEST_DATABASE)

@pytest.fixture
def client(app_context_fixture):
    return app_context_fixture.test_client()

@pytest.fixture(scope="module")
def token():
    token = jwt.encode({'public_id' : TEST_USER.public_id, 
                    'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=MAX_TEST_LENGTH)},
                    SECRET_KEY)
    return token

@pytest.fixture
def secret_key(monkeypatch, request):
    monkeypatch.setattr("Flask_REST.authorization.auth.SECRET_KEY", request.param)

@pytest.fixture
def json_body_fixture(monkeypatch,request):
    def patch_func():
        return json.dumps(request.param) 
    monkeypatch.setattr("Flask_REST.endpoints.request_checks.checkForJsonBody.request.get_json",
    patch_func)

@pytest.fixture
def content_type_fixture(request):
    try:
        return request.param
    except:
        return 'application/json'

@pytest.fixture
def request_context_fixture(app_context_fixture, token, content_type_fixture, test_logger):
    """Create flask request context"""
    key, val = "article_url", "www.website.com"
    data={}
    data[key] = val
    body = json.dumps(data)

    with app_context_fixture.test_request_context(headers={'x-access-token': token,
                                                    'Content-Type': content_type_fixture},
                                                    json=body):
        yield

@pytest.fixture
def test_logger():
    import logging
    TEST_LOG_FILE = "TEST_LOG.log"
    logger = logging.getLogger("TEST_LOGGER")
    file_handler = logging.FileHandler(TEST_LOG_FILE)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    yield logger
    os.remove(TEST_LOG_FILE)
