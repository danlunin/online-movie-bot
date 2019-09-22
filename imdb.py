import json
from requests import get

IMDB_API = 'http://www.omdbapi.com/?t='
API_KEY = 'b7deeb22'


def parse_imdb_data(data):
    return json.loads(data)


def get_imdb_data(film_name, api_key=API_KEY):
    description = get(IMDB_API + film_name + '&apikey=' + api_key)
    return description.text
