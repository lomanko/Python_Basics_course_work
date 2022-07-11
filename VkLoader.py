import requests
from datetime import datetime
from pathlib import Path
import time


class VkLoader:  # класс для работы с API VK

    url = 'https://api.vk.com/method/'  # общая ссылка на API

    def __init__(self, vktoken, version):  # init для параметров (токен и версия API)
        self.params = {'access_token': vktoken,
                       'v': version}

    def get_albums_id(self, owner_id=None):  # функция для метода запроса информации по альбомам пользователя
        album_id_url = self.url + 'photos.getAlbums'
        load_photo_params = {
            'owner_id': owner_id}
        req = requests.get(album_id_url, params={**self.params, **load_photo_params}).json()
        return req

    def vk_load_photo(self, owner_id=None, album_id='profile', count=5):
        """
        Функция получает словарь типа:
        ключ - название фото (кол-во лайков + расширение)
        Если количество лайков одинаково, то в название добавляется дата загрузки фото;
        значение - список: ссылка на фото и код размера
        """
        load_photo_url = self.url + 'photos.get'  # ссылка на метод API VK photos.get
        load_photo_params = {  # параметры метода
            'owner_id': owner_id,
            'album_id': album_id,
            'photo_sizes': 1,
            'extended': 1,
            'rev': 0,
            'count': count
        }
        req = requests.get(load_photo_url, params={**self.params, **load_photo_params}).json()  # запрос к методу API
        if req.get('error'):  # обработка случая, если результат метода возвращает ошибку
            print(f'Ошибка получения фото VK, сообщение об ошибке: {req["error"]["error_msg"]}')
            return 'Error'
        req_items = req['response']['items']
        photo_vk = []

        for item in req_items:  # получаем список с данными о количестве лайков
            photo_likes = item['likes']['count']  # получаем количество лайков у фото
            photo_vk.append(photo_likes)

        photo_vk_dict = {}
        count_for_photo = 0  # счётчик, если есть фото с одинаковым количеством лайков и созданные в одно время
        for item in req_items:
            photo_url = self.vk_find_max_size(item['sizes'])[0]  # получаем ссылку на фото максимального размера
            photo_size = self.vk_find_max_size(item['sizes'])[1]  # получаем код размера
            photo_likes = item['likes']['count']  # получаем количество лайков у фото
            photo_load_date = datetime.fromtimestamp(item['date'])  # получаем дату загрузки фото
            format_data = "%d_%b_%Y_%H_%M_%S"
            photo_load_date = datetime.strftime(photo_load_date, format_data)
            photo_extension = Path(photo_url).suffixes[0].split('?')[0]  # получаем расширение фото
            # создадим словарь типа: название фото - список: ссылка и код размера
            # если несколько фото с одинаковым количеством лайков, то к названию добавляется дата загрузки фото
            count_likes = photo_vk.count(photo_likes)
            if count_likes != 1:
                photo_vk_dict[(str(photo_likes) + '_' + str(photo_load_date) + str(count_for_photo) + photo_extension)] = [photo_url, photo_size]
                count_for_photo += 1
            else:
                photo_vk_dict[(str(photo_likes) + photo_extension)] = [photo_url, photo_size]
            print(f'''Фотография номер {len(photo_vk_dict)} получена с сайта vk.com. Всего получено {len(photo_vk_dict)} фотографий.''')
            time.sleep(.1)

        return photo_vk_dict

    def get_photos_json(self, photo_vk_dict):
        """
        Из словаря для загрузки получает нужный json
        """
        photo_json = []
        for key, value in photo_vk_dict.items():
            photo_json.append({'file_name': key, 'size': value[1]})

        return photo_json

    @staticmethod
    def vk_find_max_size(size_list):
        """
        Функция принимает на вход список ссылок разного размера и возвращает ссылку максимального размера и код размера
        """
        vk_photo_sizes = {
            's': 1,
            'm': 2,
            'x': 3,
            'o': 4,
            'p': 5,
            'q': 6,
            'r': 7,
            'y': 8,
            'z': 9,
            'w': 10,
        }  # список возможных размеров фото
        max_size_url = ''
        size = 0
        size_code = None
        for photo in size_list:
            if vk_photo_sizes[photo['type']] > size:
                max_size_url = photo['url']
                size = vk_photo_sizes[photo['type']]
                size_code = photo['type']
        return [max_size_url, size_code]
