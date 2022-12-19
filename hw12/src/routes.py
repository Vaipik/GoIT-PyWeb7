from aiohttp import web

import src.views


def setup_routes(app: web.Application):
    app.add_routes(
        [
            web.get("/", src.views.index, name="index"),
            web.get("/profile", src.views.profile, name="profile"),
            web.get("/login", src.views.login, name="login"),
            web.get("/register", src.views.register, name="register")
        ]
    )
