import requests
import time
import os


class YaDiskUploader:  # класс для работы с API ЯндексДиск

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': 'OAuth {}'.format(self.token)}

    url = 'https://cloud-api.yandex.net/v1/disk/resources/'  # общая ссылка на метод API ЯндексДиск

    def create_folder(self, folder_name):  # функция для создания папки на Яндекс Диске
        params = {'path': folder_name}
        headers = self.get_headers()
        req = requests.put(self.url, headers=headers, params=params)
        return req

    def load_photos_to_disk(self, photo_url, photo_name, folder_name):
        """
        Функция загружает фотографию на Яндекс Диск.
        На вход принимает: ссылку на фото, имя для фото на Яндекс Диске и папку для сохранения
        """
        url_load = self.url + 'upload'
        headers = self.get_headers()
        params = {'url': photo_url, 'path': f'{folder_name}/{photo_name}', 'disable_redirects': 'false'}
        req = requests.post(url_load, headers=headers, params=params)
        time.sleep(.33)
        return req

    def get_file_name(self, file_path):  # получаем имя файла из ссылки на него
        return os.path.basename(file_path)

    def upload_file(self, folder, file_path):  # функция для загрузки файла на Яндекс диск
        # получаем ссылку для загрузки файла
        url_load = self.url + 'upload'
        headers = self.get_headers()
        params = {"path": f'{folder}/{self.get_file_name(file_path)}', "overwrite": "true"}
        req = requests.get(url_load, headers=headers, params=params)
        if req.status_code == 200:
            # загружаем файл
            href = req.json().get("href")  # ссылка для загрузки
            req = requests.put(href, data=open(file_path, 'rb'))
            req.raise_for_status()
            print('Файл загружен успешно')
        else:
            print(f'Ошибка загрузки файла. Сообщение об ошибке: {req.json()["message"]}')

        return req
