from aiohttp import web, ClientSession
from aiohttp_jinja2 import render_template


async def index(request):

    urls = {
        "pb24": "https://api.privatbank.ua/p24api/exchange_rates?json&date=01.12.2014",
        "mono": "https://api.monobank.ua/bank/currency"
    }
    banks = {}
    async with ClientSession() as session:
        for url in urls:
            try:
                response = await session.get(urls.get(url))
                if response.status == 200:
                    banks[url] = await response.json()
            except Exception as e:
                print(e)

        return render_template("pages/index.html", request, {"banks": banks})


    # return web.Response(text="awaited_response")


async def profile(request):
    return web.Response(text="profile page")


async def login(request):
    return web.Response(text="login page")


async def register(request):
    return web.Response(text="register page")
