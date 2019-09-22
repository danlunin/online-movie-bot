from bs4 import BeautifulSoup
from requests import get
import html.parser
from language_utils import encode_russian

GOOGLE_QUERY = 'https://www.google.com/search?q='
KINOPOISK_QUERY = 'https://www.kinopoisk.ru/index.php?kp_query='


def get_english_name_google(film_name):
    query = GOOGLE_QUERY + 'кинопоиск' + '+' + film_name
    print(query)
    google = get(query)
    soup = BeautifulSoup(google.text, 'lxml')

    for h in soup.findAll('span', attrs={'class': 'st'}):
        splitted_link = str(h).split('—')
        link = splitted_link[1] if len(splitted_link) > 1 else splitted_link[0]
        link = link.replace('<b>', '').replace('</b>', '').replace('<br/>', '')
        link = link[:link.index('.')] if link.find('.') != -1 else link
        print(link)
        eng_name = html.parser.HTMLParser().unescape(link)
        print(eng_name)
        return eng_name


def get_english_name_kinopoisk(russian_name):
    encoded = encode_russian(russian_name)
    print(encoded)
    description = get(KINOPOISK_QUERY + encoded + "&what=")
    soup = BeautifulSoup(description.text, 'lxml')
    for h in soup.findAll('span', attrs={'class': 'gray'}):
        h = str(h)
        start = str(h).index(">")
        eng_name = h[start + 1:].split(",")[0]
        print(eng_name)
        return eng_name


def extract_link_watch(film_name):
    query = GOOGLE_QUERY + \
            '%D1%81%D0%BC%D0%BE%D1%82%D1%80%D0%B5%D1%82%D1%8C+' \
            '%D0%BE%D0%BD%D0%BB%D0%B0%D0%B9%D0%BD' \
            + film_name + \
            '%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE'
    print(query)
    google = get(query)
    soup = BeautifulSoup(google.text, 'lxml')
    for h in soup.findAll('h3', attrs={'class': 'r'}):
        link = str(h.find('a'))
        link = link[:link.index('&amp')] if link.find('&amp') != -1 else link
        print(link)
        return link
