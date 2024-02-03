import time
from datetime import datetime

import requests


def get_season(season=None, year=None, type_=None, now=False) -> tuple:
    """
        Returns a tuple of dictionaries with anime of a given season or the
        current season
    """

    if year is not None:
        assert year > datetime.now().year, "Year can't be more than current year"
        assert year > 1980, "Year is too little"

    if not now and season not in ('winter', 'spring', 'summer', 'fall'):
        raise ValueError(f'Wrong value of season parameter: {season}')

    if now and (year is not None or season is not None):
        raise ValueError('Wrong parameters')

    if not now and (year is None or season is None):
        raise ValueError('Year or season is None!')

    p = {'filter': None, 'page': 1}

    if type_ is None:
        p['filter'] = 'tv'
    elif type_ in ('movie', 'ova', 'special', 'ona', 'music'):
        p['filter'] = type_
    else:
        raise ValueError(f'No such type "{type_}" in anime database')

    if now:
        url = 'https://api.jikan.moe/v4/seasons/now'
    else:
        url = f'https://api.jikan.moe/v4/seasons/{year}/{season}'

    resp_body = requests.get(url, params=p).json()
    print(url)
    # print(resp_body)

    data = resp_body['data']

    while resp_body['pagination']['has_next_page']:
        p['page'] += 1
        resp_body = requests.get(url, params=p).json()
        data.extend(resp_body['data'])

    return tuple(data)

def get_genres():
    pass