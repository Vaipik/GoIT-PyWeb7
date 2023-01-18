from fastapi import FastAPI

from api.routers import articles, users


app = FastAPI(
    title="RESTApi",
    description="Authentication via JWT",
    version="0.1.0",
)


app.include_router(articles.router)
# app.include_router(currencies.router)
app.include_router(users.router)
