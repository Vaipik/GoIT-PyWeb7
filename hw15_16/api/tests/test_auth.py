from fastapi import status
from fastapi.testclient import TestClient
import pytest

auth_url = "/token"


@pytest.mark.run(after="test_post_users_422")
def test_post_auth_422(client: TestClient):
    response = client.post(auth_url, json={"user": "admin", "password": "pass"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_post_auth_401(client: TestClient):
    response = client.post(auth_url, data={"username": "admin", "password": "password"})
    print(response.json())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
