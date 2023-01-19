from fastapi import status

from .conftest import test_app


def test_get_all_articles_404():
    """When no articles"""
    response = test_app.get("/articles")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"message": "No articles were found"}


def test_get_article():
    pass