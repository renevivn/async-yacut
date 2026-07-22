from datetime import datetime

from yacut import db

from .constants import MAX_SHORT_ID_LENGTH


class URLMap(db.Model):
    """Модель для хранения ссылок."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(MAX_SHORT_ID_LENGTH),
        index=True,
        unique=True,
        nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @classmethod
    def create(cls, original, short):
        """
        Создаёт новую запись URLMap и добавляет её в сессию.

        Без commit — нужно для пакетного сохранения нескольких файлов
        в files_view одним запросом.
        """
        url_map = cls(original=original, short=short)
        db.session.add(url_map)
        return url_map