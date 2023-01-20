from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
import pytest


articles_url = "/articles"
auth_url = "/token"

articles = {}  # for get, put and delete methos {"uuid": uuid}


def test_get_all_articles_404(client: TestClient):
    """When no articles"""
    response = client.get(articles_url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"message": "No articles were found"}


def test_get_article_404(client: TestClient):
    """When no given article"""
    _uuid = uuid4()
    response = client.get(f"{articles_url}/{_uuid}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "uuid": str(_uuid),
        "message": "Article with given uuid was not found",
    }


def test_post_article_401(client: TestClient):
    response = client.post(articles_url, json={"title": "no matter", "text": "matter"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_put_article_401(client: TestClient):
    response = client.put(f"{articles_url}/asd", json={"no matter": "no matter"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_article_401(client: TestClient):
    response = client.delete(f"{articles_url}/{'asdasasd'}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.run(after="test_post_auth_401")
def test_post_article_201(client: TestClient, headers):
    response = client.post(
        articles_url,
        json={
            "title": "How to create api?",
            "text": "Some article text",
        },
        headers=headers,
    )
    articles.update(response.json())
    assert response.status_code == status.HTTP_201_CREATED


def test_post_article_422(client: TestClient, headers):
    response = client.post(articles_url, json={"title": "title"}, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_article_before_put_200(client: TestClient):
    _uuid = articles["uuid"]
    response = client.get(f"{articles_url}/{_uuid}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == articles


def test_put_article_422(client: TestClient, headers):
    _uuid = articles["uuid"]
    response = client.put(
        f"{articles_url}/{_uuid}4", json={"addd": "add"}, headers=headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_put_article_404(client: TestClient, headers):
    _uuid = uuid4()
    response = client.put(
        f"{articles_url}/{_uuid}", json={"addd": "add"}, headers=headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_put_article_200(client: TestClient, headers):
    _uuid = articles["uuid"]
    response = client.put(
        f"{articles_url}/{_uuid}", json={"title": "add"}, headers=headers
    )
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_json["title"] == "add"
    assert response_json["text"] == articles["text"]
    assert response_json["created_at"] == articles["created_at"]
    assert response_json["uuid"] == _uuid
    assert response_json["edited_at"] is not None


def test_delete_article_422(client: TestClient, headers):
    _uuid = uuid4()
    response = client.delete(f"{articles_url}/{_uuid}4", headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_article_404(client: TestClient, headers):
    _uuid = uuid4()
    response = client.delete(f"{articles_url}/{_uuid}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_article_204(client: TestClient, headers):
    _uuid = articles["uuid"]
    response = client.delete(f"{articles_url}/{_uuid}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
