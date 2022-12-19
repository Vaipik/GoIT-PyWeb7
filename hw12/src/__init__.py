from aiohttp import web
import aiohttp_jinja2
import jinja2

from src import routes, settings


def create_app():

    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("templates"))
    app["config"] = settings.config
    app["dbsession"]
    routes.setup_routes(app)

    return app


if __name__ == "__main__":

    app = create_app()
    web.run_app(
        app=app,
        host="localhost",
        port=5000
    )
