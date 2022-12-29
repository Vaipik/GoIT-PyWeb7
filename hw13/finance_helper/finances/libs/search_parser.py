def parse_search_request(data: str) -> tuple[list[str], list[float]]:
    """

    :param data: search field input data
    :return: One tuple contains two lists.
    """
    numbers = []
    words = []

    for item in data.split():

        try:
            numbers.append(float(item))
        except ValueError:
            pass

        if item.isalpha():
            words.append(item)

    return words, numbers
