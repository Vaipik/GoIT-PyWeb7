from time import sleep

from bs4 import BeautifulSoup
import requests
from sqlalchemy.exc import IntegrityError

from src.storage import models, db


def parse() -> list[dict]:
    """
    Return list with items
    :return:
    """
    data = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
    }

    query = {
        'q': 'французкий бульдог',
        'p': 1,
    }

    url = 'https://www.olx.ua/d/uk/zhivotnye/sobaki/'
    r = requests.get(url, headers=headers, params=query)
    bs = BeautifulSoup(r.text, 'html.parser')
    pages = len(bs.select('a.css-1mi714g'))  # Кількість сторінок
    start_index = 0

    for page in range(1, pages + 1):
        sleep(1)
        print(f"Searching info on {page} of {pages}...")
        r = requests.get(url, headers=headers, params=query)
        bs = BeautifulSoup(r.text, 'html.parser')
        query['page'] = page + 1
        dogs = bs.find_all('div', class_='css-u2ayx9')
        """
            Назва оголошення
            Ціна оголошення
        """
        for dog in dogs:

            dog_title = dog.find('h6', class_='css-ervak4-TextStyled er34gjf0').get_text()
            if dog.find('p', class_="css-1667irc-TextStyled er34gjf0") is None:  # Якщо ціни немає
                dog_price = 'No price'
            else:
                dog_price = ', '.join([price.replace('грн.', '').strip()
                                       for price in dog.find('p', class_="css-1667irc-TextStyled er34gjf0").strings])

            data.append(
                {
                    'title': dog_title,
                    'price': dog_price,
                }
                )

        dogs = bs.find_all('p', class_='css-1rsg3ca-TextStyled er34gjf0')  # Місце розташування
        for idx, dog in enumerate(dogs, start_index):
            data[idx]['location'] = dog.get_text()

        dogs = bs.find_all('a', class_='css-rc5s2u')
        """
            Посилання на оголошення
        """
        for idx, link in enumerate(dogs, start_index):
            data[idx]['url'] = f"https://olx.ua{link.get('href')}"

        start_index = idx + 1

    data = list(filter(lambda dog: 'extended' not in dog['url'], data))
    return data


def save_db(data: list[dict]) -> None:
    print("Writing data to db...")
    for advertisment in data:
        puppy = models.Advertisment(
            **advertisment
        )
        try:
            db.session.add(puppy)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()

    print("Done!")


if __name__ == '__main__':

    save_db(
        parse()
    )
