from datetime import datetime
from src.repository.currency import CurrencyCRUD


async def normalize_json(session, response_json: list[dict]) -> list[dict]:
    """
    This function is used to replace currency codes to their names.\n
    :param session:
    :param response_json: response from monobank api, should be list of dictionaries
    :return: list of dictionaries with replaced currency codes
    """
    result = []
    for cur in response_json:
        if cur["currencyCodeB"] == 980:
            if cur.get("rateBuy"):
                result.append(
                    {
                        "currency": await CurrencyCRUD.get_currency_name(session, cur["currencyCodeA"]),
                        "rate_buy": cur["rateBuy"],
                        "rate_sell": cur["rateSell"],
                        "date": datetime.fromtimestamp(cur["date"]).date()
                    }
                )

    return result
