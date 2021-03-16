""" Pytest test functions for both endpoints """
import requests

CHANNEL_ENDPOINT = "http://localhost:5000/v1/channels"
ARTICLE_ENDPOINT = "http://localhost:5000/v1/articles"

TEST_URL = "https://www.visitfinland.com/"

TEST_CHANNEL_NAME = "TEST_CHANNEL"
TEST_UPDATED      = "TEST_CHANNEL_UPDATED"
TEST_ARTICLE_NAME = "TEST_ARTICLE"

ERROR_PARAMETER = "ERROR_ON_PURPOSE"

def test_channels_post():
    response = requests.post(CHANNEL_ENDPOINT)
    assert response.status_code == 400 # Bad request - no channel name provided
    response = requests.post(CHANNEL_ENDPOINT, json={"channel_name": TEST_CHANNEL_NAME})
    assert response.status_code == 201 # Should succeed 
    response = requests.post(CHANNEL_ENDPOINT, json={"channel_name": TEST_CHANNEL_NAME})
    assert response.status_code == 400 # Bad request - channel already exists (not mandatory)

def test_channels_put():
    response = requests.put(CHANNEL_ENDPOINT, params={"channel_name": TEST_UPDATED})
    assert response.status_code == 400 # Channel not found 
    response = requests.put(CHANNEL_ENDPOINT, json={}, params={"channel_name": TEST_CHANNEL_NAME})
    assert response.status_code == 400 # Found channel but not provided with updated name
    response = requests.put(CHANNEL_ENDPOINT, json = {"channel_name": TEST_UPDATED}, params={"channel_name": TEST_CHANNEL_NAME})
    assert response.status_code == 200 # Update the channel name
    response = requests.put(CHANNEL_ENDPOINT, json = {"channel_name": TEST_CHANNEL_NAME}, params={"channel_name": TEST_UPDATED})
    assert response.status_code == 200 # Update back to TEST_CHANNEL_NAME

def test_channels_get():
    response = requests.get(CHANNEL_ENDPOINT, params={"channel_name": ERROR_PARAMETER})
    assert response.status_code == 404 
    response = requests.get(CHANNEL_ENDPOINT, params={"channel_name": TEST_CHANNEL_NAME})
    assert response.status_code == 200
    assert response.json()['channel'] == TEST_CHANNEL_NAME
    response = requests.get(CHANNEL_ENDPOINT)
    assert TEST_CHANNEL_NAME in response.json()["channels"]

def test_channels_delete():
    response = requests.delete(CHANNEL_ENDPOINT, params={"channel_name": ERROR_PARAMETER})
    assert response.status_code == 404
    response = requests.delete(CHANNEL_ENDPOINT, params={"channel_name": TEST_CHANNEL_NAME})
    assert response.status_code == 200

def test_articles_post():
    response = requests.post(ARTICLE_ENDPOINT)
    assert response.status_code == 400 # No Article URL provided
    response = requests.post(ARTICLE_ENDPOINT, json={"article_url": ERROR_PARAMETER})
    assert response.status_code == 400 # Malformed URL
    response = requests.post(ARTICLE_ENDPOINT, json={"article_url": "https://www.f.com"})
    assert response.status_code == 404 # Non-existent URL
    response = requests.post(ARTICLE_ENDPOINT, json={"article_url": TEST_URL})
    assert response.status_code == 201 # Create a valid entry (Not idempotent)

def test_articles_get():
    response = requests.get(ARTICLE_ENDPOINT)
    assert len(response.json()) == 1 and response.json()[0]["article_url"] == TEST_URL
    response = requests.get(ARTICLE_ENDPOINT, params={"article_url": ERROR_PARAMETER})
    assert response.status_code == 404 # Non-existent article
    response = requests.get(ARTICLE_ENDPOINT, params={"article_url": TEST_URL})
    assert response.status_code == 200

def test_articles_put():
    response = requests.put(ARTICLE_ENDPOINT, json={})
    assert response.status_code == 400
    response = requests.put(ARTICLE_ENDPOINT, params={"article_url": ERROR_PARAMETER})
    assert response.status_code == 400
    response = requests.put(ARTICLE_ENDPOINT, json={"channel_name": TEST_CHANNEL_NAME}, params={"article_url": TEST_URL})
    assert response.status_code == 200
    requests.put(ARTICLE_ENDPOINT, json={"channel_name": TEST_CHANNEL_NAME}, params={"article_url": TEST_URL}) # repeat to check for idempotency
    response = requests.get(ARTICLE_ENDPOINT, params={"article_url": TEST_URL})
    assert len(response.json()["channels"]) == 1 # Repeated calls does not result in channel duplicates

def test_articles_patch():
    response = requests.patch(ARTICLE_ENDPOINT, json={})
    assert response.status_code == 400
    response = requests.patch(ARTICLE_ENDPOINT, params={"article_url": ERROR_PARAMETER})
    assert response.status_code == 400
    response = requests.patch(ARTICLE_ENDPOINT, params={"article_url": ERROR_PARAMETER}, json={"channel_name": TEST_CHANNEL_NAME})
    assert response.status_code == 404
    response = requests.patch(ARTICLE_ENDPOINT, params={"article_url": TEST_URL}, json={"channel_name": TEST_CHANNEL_NAME})
    assert response.status_code == 200
    response = requests.get(ARTICLE_ENDPOINT, params={"article_url": TEST_URL})
    assert len(response.json()["channels"]) == 0
    requests.delete(CHANNEL_ENDPOINT, params={"channel_name": TEST_CHANNEL_NAME}) # clean up created channel 

def test_articles_delete():
    response = requests.delete(ARTICLE_ENDPOINT)
    assert response.status_code == 400
    response = requests.delete(ARTICLE_ENDPOINT, params={"article_url": ERROR_PARAMETER})
    assert response.status_code == 404
    response = requests.delete(ARTICLE_ENDPOINT, params={"article_url": TEST_URL})
    assert response.status_code == 200
