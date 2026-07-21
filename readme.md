# YaCut

# **Описание**

YaCut — сервис укорачивания ссылок. Пользователи могут превращать длинные ссылки в короткие.
Можно получить короткую ссылку, как предложив свой вариант, так и получив его автоматически.
Дополнительная функция сервиса — асинхронная загрузка нескольких файлов на Яндекс Диск с генерацией коротких ссылок для их скачивания.

Проект предоставляет как веб-интерфейс, так и REST API для создания и получения коротких ссылок.

# **Использованные технологии**

- [Python 3.12](https://docs.python.org/3.12/) — язык программирования
- [Flask](https://flask.palletsprojects.com/) — backend-фреймворк
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) — ORM для работы с базой данных
- [Flask-Migrate](https://flask-migrate.readthedocs.io/) — управление миграциями базы данных
- [Flask-WTF](https://flask-wtf.readthedocs.io/) — работа с формами и CSRF-защита
- [aiohttp](https://docs.aiohttp.org/) — асинхронные запросы к API Яндекс Диска
- [SQLite](https://www.sqlite.org/docs.html) — база данных
- [Jinja2](https://jinja.palletsprojects.com/) — шаблонизатор
- [Bootstrap](https://getbootstrap.com/) — вёрстка интерфейса
- [Git](https://git-scm.com/docs) — система контроля версий

# **Установка**

- Клонировать репозиторий и перейти в него:

```git clone https://github.com/renevivn/async-yacut```
```cd yacut```

- Создать и активировать виртуальное окружение:

```python -m venv venv```
```source venv/Scripts/activate```

- Установить зависимости:

```pip install -r requirements.txt```

- Создать файл `.env` в корне проекта и заполнить переменные окружения:

```env
FLASK_APP=yacut
FLASK_DEBUG=1
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your_yandex_disk_token
```

- Применить миграции:

```
flask db upgrade
```

- Запустить проект:

```
flask run
```

# **Примеры запросов**

- Создание короткой ссылки:

POST /api/id/

```json
{
  "url": "https://practicum.yandex.ru/",
  "custom_id": "practicum"
}
```

Ответ:

```json
{
  "url": "https://practicum.yandex.ru/",
  "short_link": "http://127.0.0.1:5000/practicum"
}
```

- Получение оригинальной ссылки по короткому идентификатору:

GET /api/id/practicum/

Ответ:

```json
{
  "url": "https://practicum.yandex.ru/"
}
```

- Пример ответа при ошибке:

```json
{
  "message": "Предложенный вариант короткой ссылки уже существует."
}
```

# Адрес проекта

http://127.0.0.1:5000/

# **Автор**

Иван Ренев
GitHub: https://github.com/renevivn
