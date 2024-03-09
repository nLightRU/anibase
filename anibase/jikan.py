import time
from datetime import datetime

import requests
from requests.exceptions import HTTPError


def get_anime(id_: int):
    assert id_ > 0, "get_anime() id must be positive"
    url = f'https://api.jikan.moe/v4/anime/{id_}'
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()['data']
    elif r.status_code == 429:
        time.sleep(3)
        r = requests.get(url)
        return r.json()['data']
    elif r.status_code == 404:
        raise HTTPError(f'anime with {id_} not exists')


def get_season(season=None, year=None, type_=None, now=False) -> tuple:
    """
        Returns a tuple of dictionaries with anime of a given season or the
        current season
    """

    if year is not None:
        assert year < datetime.now().year, "Year can't be greater than current year"
        assert year > 1970, "Year is too little"

    if not now and season not in ('winter', 'spring', 'summer', 'fall'):
        raise ValueError(f'Wrong value of season parameter: {season}')

    if now and (year is not None or season is not None):
        raise ValueError('Wrong parameters')

    if not now and (year is None or season is None):
        raise ValueError('Year or season is None!')

    p = {'filter': None, 'page': 1}

    def month_to_season(m):
        if m in (1, 2, 12):
            return 'winter'
        elif m in (3, 4, 5):
            return 'spring'
        elif m in (6, 7, 8):
            return 'summer'
        elif m in (9, 10, 11):
            return 'fall'

    def add_season_year(dat, s, y, n):
        if n:
            y, s = datetime.now().year, month_to_season(datetime.now().month)
        for d in dat:
            d['season'] = s
            d['year'] = y

    if type_ is None:
        p['filter'] = 'tv'
    elif type_ in ('tv', 'movie', 'ova', 'special', 'ona', 'music'):
        p['filter'] = type_
    else:
        raise ValueError(f'No such type "{type_}" in anime database')

    if now:
        url = 'https://api.jikan.moe/v4/seasons/now'
    else:
        url = f'https://api.jikan.moe/v4/seasons/{year}/{season}'

    resp_body = requests.get(url, params=p)

    if resp_body.status_code == 200:
        resp_body = resp_body.json()
        data = resp_body['data']
        if type_ in ('movie', 'ova', 'special', 'ona', 'music'):
            add_season_year(data, season, year, now)
    else:
        raise Exception('Bad request')

    flag = True
    while resp_body['pagination']['has_next_page']:
        if flag:
            p['page'] += 1
        resp_body = requests.get(url, params=p)
        if resp_body.status_code == 200:
            resp_body = resp_body.json()
            if type_ in ('movie', 'ova', 'special', 'ona', 'music'):
                add_season_year(data, season, year, now)
            data.extend(resp_body['data'])
            flag = True
        else:
            flag = False
            time.sleep(1)

    return tuple(data)


# def get_season_all(season, year, now):
#     if year is not None:
#         assert year < datetime.now().year, "Year can't be greater than current year"
#         assert year > 1970, "Year is too little"
#
#     if not now and season not in ('winter', 'spring', 'summer', 'fall'):
#         raise ValueError(f'Wrong value of season parameter: {season}')
#
#     if now and (year is not None or season is not None):
#         raise ValueError('Wrong parameters')
#
#     if not now and (year is None or season is None):
#         raise ValueError('Year or season is None!')
#
#     data = []
#     for t in ('tv', 'movie', 'ova'):
#         data.extend(get_season(season, year, type_=t, now=now))
#     time.sleep(2)
#     for t in ('special', 'ona', 'music'):
#         data.extend(get_season(season, year, type_=t, now=now))
#     return tuple(data)


def get_genres():
    url = 'https://api.jikan.moe/v4/genres/anime'

    genres = []
    for x in ('genres', 'themes', 'demographics', 'explicit_genres'):
        try:
            r = requests.get(url, params={'filter': x})
            genres.extend(r.json()['data'])
        except HTTPError as error:
            print(f'get_genres() HTTP Error occurred: {error}')
        time.sleep(1)

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
