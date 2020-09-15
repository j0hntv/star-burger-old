import requests
from django.conf import settings
from django.core.cache import cache


APIKEY = settings.YANDEX_GEOCODER_KEY


def fetch_coordinates(place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": APIKEY, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def add_coordinates(queryset):
    cache_coordinates = cache.get_many(item.address for item in queryset)
    noncache_coordinates = {}

    for item in queryset:
        coordinates = cache_coordinates.get(item.address)
        if not coordinates:
            coordinates = fetch_coordinates(item.address)
            noncache_coordinates[item.address] = coordinates

        item.coordinates = coordinates

    cache.set_many(noncache_coordinates)
    return queryset
