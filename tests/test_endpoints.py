""" Pytest test functions """
from flask import request
from base64 import b64encode

CHANNEL_ENDPOINT = "/v1/channels/"
ARTICLE_ENDPOINT = "/v1/articles/"
LOGIN_ENDPOINT   = "/login/"

TEST_URL = "https://www.visitfinland.com/"

TEST_CHANNEL_NAME = "TEST_CHANNEL"
TEST_UPDATED      = "TEST_CHANNEL_UPDATED"

ERROR_PARAMETER = "ERROR_ON_PURPOSE"

def test_login(client):
    credentials = b64encode(b"root:admin_password").decode('utf-8')
    response  = client.post(LOGIN_ENDPOINT, headers={"Authorization": f"Basic {credentials}"})
    assert response.get_json()["token"] is not None

def test_channels_post(client, token, request_context_fixture):
    response = client.post(CHANNEL_ENDPOINT, headers={'Content-Type': 'application/json',
                                            'x-access-token': token})
    assert response.status_code == 400 # Bad request - no channel name provided
    response = client.post(CHANNEL_ENDPOINT, headers={'x-access-token': token},
                                             json={'channel_name': TEST_CHANNEL_NAME})
    assert response.status_code == 201 # Should succeed
    
    response = client.post(CHANNEL_ENDPOINT, headers={'x-access-token': token},
                                            json={"channel_name": TEST_CHANNEL_NAME})
    assert response.status_code == 200 # channel already exists (succeeds but not double entries)

def test_channels_put(client, token, request_context_fixture):
    response = client.put(CHANNEL_ENDPOINT + ERROR_PARAMETER, headers={'Content-Type': 'application/json',
                                            'x-access-token': token})
    assert response.status_code == 400 # Channel not found 
    response = client.put(CHANNEL_ENDPOINT + TEST_CHANNEL_NAME,headers={'x-access-token': token}, 
                                                            json={})
    assert response.status_code == 400 # Found channel but not provided with updated name
    response = client.put(CHANNEL_ENDPOINT + TEST_CHANNEL_NAME,headers={'x-access-token': token},
                                                            json = {"channel_name": TEST_UPDATED})
    assert response.status_code == 200 # Update the channel name
    response = client.put(CHANNEL_ENDPOINT + TEST_UPDATED, headers={'x-access-token': token},
                                                        json = {"channel_name": TEST_CHANNEL_NAME})
    assert response.status_code == 200 # Update back to TEST_CHANNEL_NAME

def test_channels_get(client, token, request_context_fixture):
    response = client.get(CHANNEL_ENDPOINT + ERROR_PARAMETER, headers={'x-access-token': token})
    assert response.status_code == 404 
    response = client.get(CHANNEL_ENDPOINT + TEST_CHANNEL_NAME, headers={'x-access-token': token})
    assert response.status_code == 200
    assert response.get_json()['channel'] == TEST_CHANNEL_NAME
    response = client.get(CHANNEL_ENDPOINT, headers={'x-access-token': token}) ###
    assert TEST_CHANNEL_NAME in response.get_json()["channels"]

def test_channels_delete(client, token, request_context_fixture):
    response = client.delete(CHANNEL_ENDPOINT + ERROR_PARAMETER, headers={'x-access-token': token})
    assert response.status_code == 404
    response = client.delete(CHANNEL_ENDPOINT + TEST_CHANNEL_NAME, headers={'x-access-token': token})
    assert response.status_code == 200

def test_articles_post(client, token, request_context_fixture):
    response = client.post(ARTICLE_ENDPOINT, headers={'x-access-token': token})
    assert response.status_code == 400 # No Article URL provided
    response = client.post(ARTICLE_ENDPOINT, headers={'x-access-token': token},
                                            json={"article_url": ERROR_PARAMETER})
    assert response.status_code == 400 # Malformed URL
    response = client.post(ARTICLE_ENDPOINT, headers={'x-access-token': token},
                                            json={"article_url": "https://www.f.com"})
    assert response.status_code == 404 # Non-existent URL
    response = client.post(ARTICLE_ENDPOINT, headers={'x-access-token': token},
                                            json={"article_url": TEST_URL})
    assert response.status_code == 201 # Create a valid entry (Not idempotent)

def test_articles_get(client, token, request_context_fixture):
    response = client.get(ARTICLE_ENDPOINT, headers={'x-access-token': token})
    assert len(response.get_json()) == 1 and response.get_json()[0]["article_url"] == TEST_URL
    TEST_ARTICLE_ID = response.get_json()[0]["article_id"]
    response = client.get(ARTICLE_ENDPOINT + ERROR_PARAMETER, headers={'x-access-token': token})
    assert response.status_code == 404 # Non-existent article
    response = client.get(ARTICLE_ENDPOINT + str(TEST_ARTICLE_ID), headers={'x-access-token': token})
    assert response.status_code == 200

def test_articles_put(client, token, request_context_fixture):
    # To get current article id
    response = client.get(ARTICLE_ENDPOINT, headers={'x-access-token': token})
    TEST_ARTICLE_ID = response.get_json()[0]["article_id"]

    response = client.put(ARTICLE_ENDPOINT, headers={'x-access-token': token}, json={})
    assert response.status_code == 400
    response = client.put(ARTICLE_ENDPOINT + ERROR_PARAMETER, headers={'x-access-token': token})
    assert response.status_code == 404
    response = client.put(ARTICLE_ENDPOINT + str(TEST_ARTICLE_ID), headers={'x-access-token': token},
                                                                 json={"channel_name": TEST_CHANNEL_NAME})
    assert response.status_code == 200
    client.put(ARTICLE_ENDPOINT + str(TEST_ARTICLE_ID), headers={'x-access-token': token}, 
                                                        json={"channel_name": TEST_CHANNEL_NAME}) # repeat to check for idempotency

    response = client.get(ARTICLE_ENDPOINT + str(TEST_ARTICLE_ID), headers={'x-access-token': token})

    assert len(response.get_json()["channels"]) == 1 # Repeated calls do not result in channel duplicates

def test_articles_patch(client, token, request_context_fixture):
    # To get current article id
    response = client.get(ARTICLE_ENDPOINT, headers={'x-access-token': token})
    TEST_ARTICLE_ID = response.get_json()[0]["article_id"]

    response = client.patch(ARTICLE_ENDPOINT, headers={'x-access-token': token}, json={})
    assert response.status_code == 400
    response = client.patch(ARTICLE_ENDPOINT + ERROR_PARAMETER, headers={'x-access-token': token})
    assert response.status_code == 404
    response = client.patch(ARTICLE_ENDPOINT + ERROR_PARAMETER, headers={'x-access-token': token},
                                                            json={"channel_name": TEST_CHANNEL_NAME})
    assert response.status_code == 404
    response = client.patch(ARTICLE_ENDPOINT + str(TEST_ARTICLE_ID), headers={'x-access-token': token}, 
                                                            json={"channel_name": TEST_CHANNEL_NAME})
    assert response.status_code == 200
    response = client.get(ARTICLE_ENDPOINT + str(TEST_ARTICLE_ID), headers={'x-access-token': token})
    assert len(response.get_json()["channels"]) == 0
    client.delete(CHANNEL_ENDPOINT + TEST_CHANNEL_NAME, headers={'x-access-token': token}) # clean up created channel 

def test_articles_delete(client, token, request_context_fixture):
    # To get current article id
    response = client.get(ARTICLE_ENDPOINT, headers={'x-access-token': token})
    TEST_ARTICLE_ID = response.get_json()[0]["article_id"]

    response = client.delete(ARTICLE_ENDPOINT, headers={'x-access-token': token})
    assert response.status_code == 400
    response = client.delete(ARTICLE_ENDPOINT + ERROR_PARAMETER, headers={'x-access-token': token})
    assert response.status_code == 404
    response = client.delete(ARTICLE_ENDPOINT + str(TEST_ARTICLE_ID), headers={'x-access-token': token})
    assert response.status_code == 200
