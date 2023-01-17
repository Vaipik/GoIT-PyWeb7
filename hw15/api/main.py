from fastapi import FastAPI

from api.routers import articles, currencies


app = FastAPI()


app.include_router(articles.router)
# app.include_router(currencies.router)
