import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .constants import RESERVED_NAMES, SHORT_ID_PATTERN
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .short_id import get_unique_short_id


@app.route('/api/id/', methods=('POST',))
def create_id():
    """Создает короткую ссылку по переданному URL через API."""
    request_data = request.get_json(silent=True)
    if request_data is None:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса',
            HTTPStatus.BAD_REQUEST
        )
    if 'url' not in request_data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!',
            HTTPStatus.BAD_REQUEST
        )
    if not request_data['url']:
        raise InvalidAPIUsage(
            '"url" не может быть пустым!',
            HTTPStatus.BAD_REQUEST
        )

    short = request_data.get('custom_id')
    if not short:
        short = get_unique_short_id()
    else:
        if not re.match(SHORT_ID_PATTERN, short):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки',
                HTTPStatus.BAD_REQUEST
            )
        if (
            URLMap.query.filter_by(short=short).first() is not None
            or short in RESERVED_NAMES
        ):
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.',
                HTTPStatus.BAD_REQUEST
            )
    original = request_data['url']
    URLMap.create(original=original, short=short)
    db.session.commit()
    return jsonify({
        'url': original,
        'short_link': url_for('redirect_view', short_id=short, _external=True)
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_url(short_id):
    """Возвращает оригинальный URL по короткому идентификатору через API."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
