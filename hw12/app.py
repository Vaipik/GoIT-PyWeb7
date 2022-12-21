from aiohttp import web

from src import create_app
from src.libs.codes_to_db import get_codes
from src.repository.currency import CurrencyCRUD


if __name__ == "__main__":

    app = create_app()

    web.run_app(
        app=app,
        host="localhost",
        port=5000
    )

    # with app["db_session"] as db_session:
    #     codes = get_codes(db_session)
    #     if codes:
    #         CurrencyCRUD.write_to_db(db_session, codes)
