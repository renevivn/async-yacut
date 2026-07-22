import random

from .constants import ALLOWED_CHARACTERS, NUMBER
from .models import URLMap


def get_unique_short_id():
    """Генерирует уникальный короткий идентификатор для ссылки."""
    while True:
        unique_short_id = ''.join(random.choices(ALLOWED_CHARACTERS, k=NUMBER))
        if URLMap.query.filter_by(short=unique_short_id).first() is None:
            break

    return unique_short_id
