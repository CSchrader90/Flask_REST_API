from flask import request
import pytest

from .conftest import SECRET_KEY, ERRONEOUS_KEY
test_list = [pytest.param(ERRONEOUS_KEY, marks=pytest.mark.xfail), 
            SECRET_KEY]

@pytest.mark.parametrize('secret_key', test_list, indirect=True)
def test_correct_token(request_context_fixture, secret_key):
    from Flask_REST.authorization.auth import verify_token
    class verify_token_test_class:
        @classmethod
        @verify_token
        def check_verify_token(self, user):
            return True
    
    verified = verify_token_test_class.check_verify_token()
    assert verified == True


from .conftest import TEST_REQUIRED_FIELD, TEST_URL
test_list_json_body = [pytest.param(('y', 'z'), marks=pytest.mark.xfail),
            (TEST_REQUIRED_FIELD, TEST_URL)]
test_list_headers = [pytest.param(('text/html'), marks=pytest.mark.xfail),
                    ('application/json')]

@pytest.mark.parametrize('json_body_fixture', test_list_json_body, indirect=True)
@pytest.mark.parametrize('content_type_fixture', test_list_headers, indirect=True)
def test_verify_json(request_context_fixture, json_body_fixture, test_logger):
    from Flask_REST.endpoints.request_checks.checkForJsonBody import verify_json
    class verify_json_test_class:
        @classmethod
        @verify_json(logger=test_logger, verb="POST", required_field=TEST_REQUIRED_FIELD)
        def check_verify_json(self):
            return True

    verified = verify_json_test_class.check_verify_json()
    assert verified == True

def test_cache(request_context_fixture, test_logger):
    from Flask_REST.caching.caching import cache, cache_key
    import datetime
    import time

    def check_same_response_repeated(test_class, time_diff, method):
        method = getattr(test_class, method)
        response1 = method()
        time.sleep(time_diff)
        response2  = method()
        return response1 == response2

    class verify_caching_test_class:
        @classmethod
        @cache.cached(key_prefix=datetime.datetime.now, timeout=1) # current time as cache key prefix
        def verify_cache_fail(self):
            return datetime.datetime.now()

        @classmethod
        @cache.cached(key_prefix=cache_key, timeout=1) # use request body as cache key prefix
        def verify_caching(self):
            return datetime.datetime.now()

    assert not check_same_response_repeated(verify_caching_test_class, 0.1, "verify_cache_fail")
    assert check_same_response_repeated(verify_caching_test_class, 0.1, "verify_caching")
