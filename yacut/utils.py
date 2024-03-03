from random import randrange

from .models import URLMap

ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def get_unique_short_id():
    unique_short_id = ''
    for _ in range(6):
        unique_short_id += ALPHABET[randrange(0, len(ALPHABET) - 1)]
    if URLMap.query.filter_by(short=unique_short_id).first():
        unique_short_id = get_unique_short_id()
    return unique_short_id