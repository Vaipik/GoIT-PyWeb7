from typing import Generator

from fastapi.testclient import TestClient
import pytest

from api.database.connection import SessionLocal
from api.app import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as client:
        yield client
