from datetime import datetime

from yacut import db


class URLMap(db.Model):
    """Модель для хранения ссылок."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), index=True, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)