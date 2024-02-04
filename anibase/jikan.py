import time
from datetime import datetime

import requests
from requests.exceptions import HTTPError


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

    data = resp_body['data']

    while resp_body['pagination']['has_next_page']:
        p['page'] += 1
        resp_body = requests.get(url, params=p).json()
        data.extend(resp_body['data'])

    return tuple(data)


def get_genres():
    url = 'https://api.jikan.moe/v4/genres/anime'

    genres = []
    for x in ('genres', 'themes', 'demographics'):
        try:
            r = requests.get(url, params={'filter': x})
            genres.extend(r.json()['data'])
        except HTTPError as error:
            print(f'get_genres() HTTP Error occurred: {error}')

    return genres


def get_producers(page: int = -1, trace: bool = False):
    url = 'https://api.jikan.moe/v4/producers'

    if page is not None:
        if page > 0:
            try:
                resp = requests.get(url, params={'page': page})
                if resp.status_code == 200:
                    return resp.json()['data']
                else:
                    print(f'BAD STATUS CODE FOR PAGE {page}')
                    return
            except HTTPError as error:
                print(f'get_producers() HTTP ERROR: {error}')

    p = {'page': 1}
    producers = []

    while p['page'] > 0:
        if trace:
            print(f"Page {p['page']}")
        data = []
        has_next_page = False
        try:
            resp = requests.get(url, params=p)
            if resp.status_code == 200:
                resp = resp.json()
            else:
                time.sleep(2)
                continue
            data, has_next_page = resp['data'], resp['pagination']['has_next_page']
        except HTTPError as error:
            print(f"get_producers() at page {p['page']} HTTP ERROR: {error}")

        producers.extend(data)
        if not has_next_page:
            p['page'] = -1
        else:
            p['page'] += 1
            if p['page'] % 3 == 0:
                time.sleep(1)

    return producers
