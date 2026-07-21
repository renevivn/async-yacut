from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, URLField
from wtforms.validators import URL, DataRequired, Optional, Regexp

from .utils import SHORT_ID_PATTERN


class URLMapForm(FlaskForm):
    """Форма для главной страницы."""

    # Поле для оригинальной длинной ссылки.
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(require_tld=False, message='Введите корретую ссылку')
        ]
    )
    # Поле для пользовательского варианта короткого идентификатора.
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Regexp(
                regex=SHORT_ID_PATTERN,
                message='Только латинские буквы и цифры, длина до 16 символов.'
            ),
        ]
    )


class FileForm(FlaskForm):
    """Форма для страницы загрузки файлов."""

    files = MultipleFileField('Выбрать файлы', validators=[FileRequired()])