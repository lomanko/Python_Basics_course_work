from VkLoader import VkLoader
from YaDiskUploader import YaDiskUploader
import json

if __name__ == '__main__':
    print(f'''Программа резервного копирования фотографий из vk на ЯндексДиск.
Токены для vk и ЯндексДиска должны быть в папке token.txt.
По умолчанию программа копирует фото из профиля, которому принадлежит токен в количестве 5 фото.''')
    with open('token.txt') as f:  # получение токенов из файла token.txt
        vk_token = f.readline().strip()
        ya_disk_token = f.readline().strip()
    version = '5.131'  # версия API VK
    vk_user = VkLoader(vk_token, version)  # создание экземпляра класса VkLoader
    count = 5
    album_id = 'profile'

    user_input = input('Хотите ли вы выбрать другие параметры загрузки (да/нет): ')
    if user_input == 'нет':
        owner_id = None
    else:
        owner_choice = input('Вы хотите получить фото из своего профиля (да/нет): ')
        if owner_choice == 'да':
            owner_id = None
        else:
            owner_id = input('Введите id пользователя для копирования фотографий: ')
        album_info = input('Получить фотографии из профиля (profile), со стены (wall) или из другого альбома (other): ')
        if album_info == 'profile' or album_info == 'wall':
            album_id = album_info
            count = input('Введите количество фотографий, которые надо скопировать: ')
        else:
            print('Список альбомов пользователя.')
            albums = vk_user.get_albums_id(owner_id=owner_id)
            if albums.get('error') is None:
                albums = vk_user.get_albums_id(owner_id=owner_id)['response']['items']
                for album in albums:
                    print(
                        f'Название альбома: {album["title"]}, ID альбома:{album["id"]}, в альбоме {album["size"]} фото')
                album_id = input('Введите ID альбома из списка выше: ')
                count = input('Введите количество фотографий, которые надо скопировать: ')
            else:
                print('У пользователя нет альбомов.')
                exit()

    print("\033[1m" + 'Получение фотографий с VK.com' + "\033[0m")
    photo_dict = vk_user.vk_load_photo(owner_id=owner_id, count=count,
                                       album_id=album_id)  # получение словаря для загрузки в файлообменник
    if photo_dict != 'Error':
        photo_json = vk_user.get_photos_json(photo_dict)  # получение json для записи в файл
        print("\033[1m" + 'Фотографии получены успешно' + "\033[0m")
        with open('photo_data.json', 'w') as f:  # формирование файла json
            json.dump(photo_json, f, indent=2)
            print("\033[1m" + 'Файл json сформирован успешно' + "\033[0m")

        print("\033[1m" + 'Загрузка фотографий на Яндекс Диск' + "\033[0m")
        album_name = input('Введите название альбома для загрузки фото: ')
        ya_disk_user = YaDiskUploader(ya_disk_token)  # создание экземпляра класса YaDiskUploader
        new_folder = ya_disk_user.create_folder(album_name)
        if new_folder.status_code == 201:
            print("\033[1m" + 'Папка для фотографий на Яндекс Диске создана успешно' + "\033[0m")
            count_photo = 1
            for key, value in photo_dict.items():
                upload_to_ya_disk = ya_disk_user.load_photos_to_disk(photo_url=value[0], photo_name=key,
                                                                     folder_name=album_name)
                if upload_to_ya_disk.status_code == 202:
                    print(f'Фотография номер {count_photo} загружена на Яндекс Диск успешно.')
                    count_photo += 1
                else:
                    print(f'Ошибка загрузки фотографии {count_photo}. Текст ошибки: {upload_to_ya_disk.json()["message"]}')
                    count_photo += 1
            print("\033[1m" + 'Фотографии загружены' + "\033[0m")
            print("\033[1m" + 'Загрузка файла json на Яндекс Диск' + "\033[0m")
            upload_to_ya_disk = ya_disk_user.upload_file(folder=album_name, file_path='photo_data.json')
        else:
            print("\033[1m" + 'Ошибка создания папки на Яндекс Диске' + "\033[0m")
            print(f'Текст ошибки: {new_folder.json()["message"]}')
