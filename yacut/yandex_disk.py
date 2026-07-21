import asyncio
import os
import urllib

import aiohttp
from dotenv import load_dotenv

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'

load_dotenv()
DISK_TOKEN = os.environ.get('DISK_TOKEN')

AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}


async def upload_file_and_get_url(session, file):
    """Загружает файл на Яндекс.Диск и возвращает ссылку для скачивания."""
    payload = {
        'path': f'app:/{file.filename}',  # noqa: E231
        'overwrite': 'True'
    }
    async with session.get(
        headers=AUTH_HEADERS,
        params=payload,
        url=REQUEST_UPLOAD_URL,
    ) as response:
        data = await response.json()
        if response.status != 200:
            raise ValueError(f'Ошибка загрузки файла: {data}')
        upload_url = data['href']

    file_content = file.read()
    async with session.put(
        data=file_content,
        url=upload_url,
    ) as response:
        if not response.ok:
            raise ValueError(
                f'Ошибка при загрузке файла на Диск: {response.status}'
            )
        location = response.headers['Location']
        location = urllib.parse.unquote(location)
        location = location.replace('/disk', '')

    async with session.get(
        headers=AUTH_HEADERS,
        params={'path': location},
        url=DOWNLOAD_LINK_URL,
    ) as response:
        data = await response.json()
        if response.status != 200:
            raise ValueError(f'Ошибка загрузки файла: {data}')

    return data['href']


async def async_upload_files_to_yandex_disk(files):
    """Асинхронно загружает несколько файлов на Яндекс.Диск."""
    if files is not None:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for file in files:
                tasks.append(
                    asyncio.ensure_future(
                        upload_file_and_get_url(session, file)
                    )
                )
            urls = await asyncio.gather(*tasks)
        return urls
