import decimal


def parse_search_request(data: str) -> tuple[list[str], list[decimal.Decimal]]:
    """

    :param data: search field input data
    :return: letters and numbers tuples. Each tuple contains string
    """
    numbers = []
    letters = []

    for item in data.split():

        try:
            numbers.append(float(item))
        except ValueError:
            pass

        if item.isalpha():
            letters.append(item)
    leters = ' '.join(letters)

    return letters, numbers
