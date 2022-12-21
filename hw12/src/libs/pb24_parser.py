def normalize_json(response_json: dict) -> list[dict]:
    """
    Is used to extract data about USD and EUR from response.\n
    :param response_json: response from pb24 api
    :returns: data about USD and EUR
    """
    result = []

    for currency in response_json["exchangeRate"]:
        if currency["currency"] in ("USD", "EUR"):
            result.append(currency)

    return result
