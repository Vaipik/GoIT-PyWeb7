from fastapi import status
from fastapi.testclient import TestClient
import pytest


users_url = "/users"


@pytest.mark.run(after="test_delete_article_401")
def test_post_users_201(client: TestClient):
    response = client.post(
        users_url,
        json={
            "username": "admin",
            "password": "password"
        }
    )
    response_json = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert response_json["is_active"] is True
    assert response_json["last_logged"] is None


def test_post_users_400(client: TestClient):
    response = client.post(
        users_url,
        json={
            "username": "admin",
            "password": "password"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "username": "admin",
        "message": "User with given username already exists"
    }


def test_post_users_422(client: TestClient):
    response = client.post(
        users_url,
        json={
            "usere": "admin",
            "passord": "password"
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
