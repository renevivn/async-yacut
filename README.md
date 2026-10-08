[Русская версия](README.ru.md)

# YaCut

## Description

YaCut is a URL shortener. Users can turn long links into short ones, either by suggesting their own short ID or by getting one generated automatically.
An extra feature is asynchronous upload of multiple files to Yandex Disk, with a short download link generated for each file.

The project provides both a web interface and a REST API for creating and resolving short links.

## Tech stack

- [Python 3.12](https://docs.python.org/3.12/)
- [Flask](https://flask.palletsprojects.com/) — web framework
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) — ORM
- [Flask-Migrate](https://flask-migrate.readthedocs.io/) — database migrations (Alembic)
- [Flask-WTF](https://flask-wtf.readthedocs.io/) — forms and CSRF protection
- [aiohttp](https://docs.aiohttp.org/) — asynchronous requests to the Yandex Disk API
- [SQLite](https://www.sqlite.org/docs.html) — database
- [Jinja2](https://jinja.palletsprojects.com/) — templating
- [Bootstrap](https://getbootstrap.com/) — UI layout

## Getting started

Clone the repository and go to the project folder:

```bash
git clone https://github.com/renevivn/async-yacut
cd async-yacut
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
source venv/Scripts/activate    # Windows (Git Bash)
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
FLASK_APP=yacut
FLASK_DEBUG=1
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your_yandex_disk_token
```

Apply migrations and run the app:

```bash
flask db upgrade
flask run
```

The app will be available at http://127.0.0.1:5000/ (file upload page: http://127.0.0.1:5000/files).

## API examples

Create a short link:

`POST /api/id/`

```json
{
  "url": "https://practicum.yandex.ru/",
  "custom_id": "practicum"
}
```

Response:

```json
{
  "url": "https://practicum.yandex.ru/",
  "short_link": "http://127.0.0.1:5000/practicum"
}
```

Get the original URL by its short ID:

`GET /api/id/practicum/`

Response:

```json
{
  "url": "https://practicum.yandex.ru/"
}
```

Error response example:

```json
{
  "message": "Предложенный вариант короткой ссылки уже существует."
}
```

## Author

Ivan Renev — [github.com/renevivn](https://github.com/renevivn)
