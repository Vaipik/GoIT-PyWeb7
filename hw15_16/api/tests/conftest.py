from typing import Generator

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.app import app
from api.config.config import app_config
from api.dependecies import get_db
from api.database.base_class import Base


SQLALCHEMY_DATABASE_URL = app_config["TEST_DB_URL"]
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    Base.metadata.drop_all(bind=engine)  # To delete all data from test db
finally:
    Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client() -> Generator:
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def headers(client: TestClient):
    user_credentials = {
        "username": "test",
        "password": "testpassword"
    }
    created_user = client.post("/users", json=user_credentials)
    response = client.post("/token", data=user_credentials).json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    return headers
