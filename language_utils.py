import urllib


def encode_russian(russian_text):
    return urllib.request.quote(russian_text.encode('cp1251'))


def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
