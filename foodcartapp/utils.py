import requests
from django.conf import settings
from django.core.cache import cache
from geopy.distance import distance


APIKEY = settings.YANDEX_GEOCODER_KEY


def cached(get_distance_func):
    def wrapper(*args, **kwargs):
        coordinates = cache.get(*args)
        if not coordinates:
            coordinates = get_distance_func(*args)
            cache.set(*args, coordinates)
        return coordinates

    return wrapper


@cached
def fetch_coordinates(place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": APIKEY, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_distance(address1, address2):
    return distance(
        fetch_coordinates(address1),
        fetch_coordinates(address2)).km
