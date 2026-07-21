from flask import jsonify, render_template

from . import app, db


class InvalidAPIUsage(Exception):
    """Исключение для ошибок, возникающих при обращении к API."""

    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Сериализует сообщение об ошибке в словарь для ответа в JSON."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Обрабатывает исключение InvalidAPIUsage и возвращает ошибку в JSON."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    """Обрабатывает ошибку 404 и отображает страницу «Не найдено»."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Обрабатывает внутреннюю ошибку сервера."""
    db.session.rollback()
    return render_template('500.html'), 500
