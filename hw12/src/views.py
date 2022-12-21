from datetime import datetime

from aiohttp import web, ClientSession
from aiohttp_jinja2 import render_template

from src.libs import mono_parser, pb24_parser
from src.repository.mono import MonoBankCRUD


async def index(request):

    if request.method == "POST":
        date = await request.post()
        date = date.get("date")  # yyyy-mm-dd
        if not date:
            return render_template("pages/index.html", request, context=None)

        pb24_date = f"{date[-2:]}.{date[5:7]}.{date[:4]}"  # dd.mm.yyyy
        mono_date = datetime.strptime(date, "%Y-%m-%d")
        urls = {
            "pb24": f"https://api.privatbank.ua/p24api/exchange_rates?json&date={pb24_date}",
            "mono": "https://api.monobank.ua/bank/currency"
        }
        banks = {}

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
                                banks[url] = await MonoBankCRUD.get_currencies_rates(db_session, mono_date)
                except Exception as e:
                    print(e)

            return render_template("pages/checker.html", request, {"banks": banks, "title": pb24_date})
    return render_template("pages/index.html", request, context=None)


async def profile(request):
    return web.Response(text="profile page")


async def login(request):
    return web.Response(text="login page")


async def register(request):
    return web.Response(text="register page")
