import random
from string import ascii_lowercase, ascii_uppercase, digits

from .models import URLMap


ALLOWED_CHARACTERS = ascii_lowercase + ascii_uppercase + digits
NUMBER = 6
RESERVED_NAMES = ['files']
SHORT_ID_PATTERN = r'^[A-Za-z0-9]{1,16}$'


def get_unique_short_id():
    """Генерирует уникальный короткий идентификатор для ссылки."""
    while True:
        unique_short_id = "".join(random.choices(ALLOWED_CHARACTERS, k=NUMBER))
        if URLMap.query.filter_by(short=unique_short_id).first() is None:
            break

    return unique_short_id
