from decimal import Decimal, InvalidOperation


def parse_search_request(data: str) -> tuple[list[str], list[Decimal]]:
    """

    :param data: search field input data
    :return: One tuple contains two lists.
    """
    numbers = []
    words = []

    for item in data.split():

        try:
            numbers.append(Decimal(item))
        except InvalidOperation:
            pass

        if item.isalpha():
            words.append(item)

    return words, numbers
