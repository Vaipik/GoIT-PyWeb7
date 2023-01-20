from fastapi import FastAPI

from api.routers import articles, users, auth


app = FastAPI(
    title="RESTApi",
    description="Authentication via JWT",
    version="0.1.0",
    docs_url="/doc"
)

app.include_router(auth.router)
app.include_router(articles.router)
app.include_router(users.router)

