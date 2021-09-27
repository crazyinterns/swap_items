import requests
import json


def parse_coordinates(coord_obj):
    coordinates = json.loads(coord_obj)
    return coordinates['long'], coordinates['lat']


def fetch_coordinates(apikey, address, kind=None):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
        "kind": "metro"
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places or (len(found_places) > 1):
        return None, None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def fetch_metro(apikey, lon=None, lat=None):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": f'{lon},{lat}',
        "apikey": apikey,
        "format": "json",
        "kind": "metro",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    most_relevant['GeoObject']
    metro_name = most_relevant['GeoObject']['name']
    return metro_name


def fetch_district(apikey, lon=None, lat=None):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": f'{lon},{lat}',
        "apikey": apikey,
        "format": "json",
        "kind": "district",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    district_name = most_relevant['GeoObject']['name']
    district_description = most_relevant['GeoObject']['description']
    return f'{district_description}, {district_name}'
