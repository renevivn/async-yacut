from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .constants import RESERVED_NAMES
from .forms import FileForm, URLMapForm
from .models import URLMap
from .short_id import get_unique_short_id
from .yandex_disk import async_upload_files_to_yandex_disk


@app.route('/', methods=('GET', 'POST'))
def index_view():
    """Главная страница: создание коротких ссылок через веб-форму."""
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    short = form.custom_id.data
    if not short:
        short = get_unique_short_id()
    else:
        existing = URLMap.query.filter_by(short=short).first()
        if existing is not None or short in RESERVED_NAMES:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)

    URLMap.create(original=form.original_link.data, short=short)
    db.session.commit()
    short_url = url_for('redirect_view', short_id=short, _external=True)
    return render_template('index.html', form=form, short_url=short_url)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    """Редирект с короткой ссылки на оригинальный URL."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)


@app.route('/files', methods=('GET', 'POST'))
async def files_view():
    """Страница загрузки файлов на Диск."""
    form = FileForm()
    if form.validate_on_submit():
        files = form.files.data
        files_list = []
        try:
            urls = await async_upload_files_to_yandex_disk(files)
        except ValueError as upload_error:
            flash(str(upload_error))
            return redirect(url_for('files_view'))
        for file, url in zip(files, urls):
            short = get_unique_short_id()
            URLMap.create(original=url, short=short)
            files_list.append({'name': file.filename, 'url': short})
        db.session.commit()
        return render_template('files.html', form=form, files_list=files_list)
    return render_template('files.html', form=form)