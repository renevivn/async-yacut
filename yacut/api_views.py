import re

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import RESERVED_NAMES, SHORT_ID_PATTERN, get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    """Создает короткую ссылку по переданному URL через API."""
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)

    short = data.get('custom_id')
    if not short:
        short = get_unique_short_id()
    else:
        if not re.match(SHORT_ID_PATTERN, short):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки',
                400
            )
        if (
            URLMap.query.filter_by(short=short).first() is not None
            or short in RESERVED_NAMES
        ):
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.',
                400
            )
    original = data.get('url')
    url_map = URLMap(original=original, short=short)
    db.session.add(url_map)
    db.session.commit()
    return jsonify({
        'url': original,
        'short_link': url_for('redirect_view', short_id=short, _external=True)
    }), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    """Возвращает оригинальный URL по короткому идентификатору через API."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
