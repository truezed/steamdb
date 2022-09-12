import faker

from random import randrange, choice, getrandbits

from aiohttp.web_urldispatcher import DynamicResource

from sgdb.db.schema import GameType

fake = faker.Faker('en_US')


def generate_games(games_num: int = 1) -> list:
    games = []

    for _ in range(games_num):
        games.append({
            "app_id": randrange(1, 9999999),
            "name": " ".join(fake.words(randrange(1, 4))),
            "type": choice(list(GameType)).value,
            "is_free": bool(getrandbits(1)),
            "package_id": randrange(1, 9999999),
            "has_trading_cards": bool(getrandbits(1)),
        })
    return games


def url_for(path: str, **kwargs) -> str:
    """
    Генерирует URL для динамического aiohttp маршрута с параметрами.
    """
    kwargs = {
        key: str(value)
        for key, value in kwargs.items()
    }
    return str(DynamicResource(path).url_for(**kwargs))
