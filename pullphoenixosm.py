import requests
from getset import *


def get_full_osm():
    url = "https://overpass-api.de/api/interpreter?data=" \
      "%28node%2832%2E6020062%2C%2D112%2E9699853%2C34%2E318%2C%2D111%2E036001%29%3B%3C%3B%29%3Bout%20meta%3B%0A"
    response = requests.get(url)
    with open('Phoenix.osm', 'wb') as outfile:
        outfile.write(response.content)


def create_sample():
    sample_data(get_osm_filename(), get_small_osm(), get_med_osm())
