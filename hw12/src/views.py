from datetime import datetime

from aiohttp import web, ClientSession
from aiohttp_jinja2 import render_template

from src.libs import mono_parser, pb24_parser
from src.repository.mono import MonoBankCRUD


async def index(request):

    urls = {
        "pb24": "https://api.privatbank.ua/p24api/exchange_rates?json&date=01.12.2014",
        "mono": "https://api.monobank.ua/bank/currency"
    }
    date = datetime.now().date()
    banks = {}
    req = await request.post()
    print(req.get("date"))
    async with ClientSession() as session:
        for url in urls:
            try:
                response = await session.get(urls.get(url))
                if response.status == 200:
                    response_json = await response.json()

                    if url == "mono":
                        async with request.app["db_session"] as db_session:
                            banks[url] = await mono_parser.normalize_json(db_session, response_json)
                            await MonoBankCRUD.write_to_db(db_session, banks[url])

                    if url == "pb24":
                        banks[url] = pb24_parser.normalize_json(response_json)
                else:
                    if url == "mono":
                        async with request.app["db_session"] as db_session:
                            banks[url] = await MonoBankCRUD.get_currencies_rates(db_session, date)

            except Exception as e:
                print(e)

        return render_template("pages/index.html", request, {"banks": banks})


async def profile(request):
    return web.Response(text="profile page")


async def login(request):
    return web.Response(text="login page")


async def register(request):
    return web.Response(text="register page")
