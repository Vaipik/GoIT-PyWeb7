from datetime import datetime


def normalize_json(response_json: list[dict]) -> list[dict]:
    """
    This function is used to replace currency codes to their names.\n
    :param response_json: response from monobank api, should be list of dictionaries
    :return: list of dictionaries with replaced currency codes
    """
    for currency in response_json:
        date = datetime.utcfromtimestamp(currency.get("date"))
        currency["currencyCodeA"] = codes.get(
            currency.get("currencyCodeA")
        )
        currency["currencyCodeB"] = codes.get(
            currency.get("currencyCodeB")
        )
        currency["date"] = date.strftime("%Y-%m-%d")

    return response_json

