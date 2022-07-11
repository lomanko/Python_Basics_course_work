# Проект «Резервное копирование фотографий с VK.com» 

## Задача:
1. Получать фотографии с профиля VK.com (а также из других альбомов пользователя).
2. Сохранять фотографии максимального размера (ширина/высота в пикселях) на Я.Диске.
3. Для названий фотографий использовать количество лайков, если количество лайков одинаково, то добавить дату загрузки.
4. Сохранять информацию по фотографиям в json-файл с результатами. 

### Входные данные:
1. Токены доступа к Vk.com и Яндекс Диску должны находиться в файле token.txt:
```javascript
vk_token
ya_disk_token
```
2. Программа запрашивает у пользователя:
- id пользователя для копирования фото (по умолчанию копируются фото владельца токена);
- альбом для копирования фото (фото профиля (по умолчанию), фото со стены или фото из альбомов пользователя);
- количество фото для копирования (по умолчанию - 5 фото);
- название папки на Яндекс Диске для сохранения фото (будет создана новая папка с введенным названием).


### Выходные данные:
1. json-файл с информацией по файлу:
```javascript
    [{
    "file_name": "34.jpg",
    "size": "z"
    }]
```
2. Измененный Я.диск, куда добавились фотографии.

#### Процесс выполнения программы сопровождается логированием.

В случае ошибки будет выведен текст ошибки.
