# Космический Телеграм

Набор скриптов для публикации фото в Telegram-канал

### Основные скрипты

- `photobot.py`
Позволяет автоматически публиковать в Telegram-канал фото из папки, находящейся в одном репозитории со скриптом с периодичностью (в ч), устанавливаемой в переменных окружения.

Вспомогательный скрипт - `get_photos.py`

- `publish_random_photo`
Позволяет поочередно с задержкой 1 с опубликовать в Telegram-канал одно или несколько фото по запросу к следующим API:
 
  1.[API SpaceX](https://github.com/r-spacex/SpaceX-API)
  
  Вспомогательный скрипт - `fetch_space_x_launch_photos.py`
  
  2.[NASA API APOD](https://github.com/nasa/apod-api)
  
  Вспомогательный скрипт - `fetch_nasa_apod_photos.py`
  
  3.[NASA API EPIC](https://epic.gsfc.nasa.gov/about/epic)
  
  Вспомогательный скрипт - `fetch_nasa_epic_photos.py`

  Также сохраняет опубликованные изображения в папки с соответствующим названием. Вспомогательный скрипт - `save_photos.py`

### Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `env.env` рядом со скриптами и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 4 переменные:
- Используемые в основных скриптах:
  
  `TG_BOT_TOKEN` (ОБЯЗАТЕЛЬНАЯ) - [Токен Telegram бота](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) 
  
  `TG_GROUP_ID` (ОБЯЗАТЕЛЬНАЯ) - [ID группы Telegram](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id) 

  `NASA_TOKEN` - [Токен NASA API](https://api.nasa.gov/). Используется в `fetch_nasa_apod_photos.py` и `fetch_nasa_epic_photos.py`
 
  `TIME_INTERVAL_H` - Периодичность публикации bзображений (в ч). Используется в `photobot.py`
  
  

### Как установить

Скачайте репозиторий целиком.

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Как запустить

#### `photobot.py`
 
Запустите скрипт консольной командой.

Команда включает следующие параметры:

`-f` (folder_name) - название папки, из которой будут публиковаться изображения (должна находиться в одной директории со скриптом). Обязательный параметр.

`-n` (number_of_photos) - количество публикуемых за раз изображений из данной папки (необязательный параметр, default = 1).

Пример команды:
```sh
python photobot.py -f yourfolder -n 2
```
Бот будет автоматически публиковать фото с периодичностью (в ч), указанной в переменной окружения `TIME_INTERVAL_H` 

#### `publish_random_photo`
  
Запустите скрипт консольной командой.

Команда может включать следующие параметры:

`-s` (source) выбрать из списка `['spacex', 'epic', 'apod']` - выбор API для запроса ссылок на изображения. Необязательный параметр. По дефолту выбирается случайно из списка.

`-l` (launch_id) - ID конкретного запуска при создании запроса к API SpaceX. Необязательный параметр. При отсутствии будет выполнен запрос фотографии(-й) с последнего запуска SpaceX. В обоих случаях, если ответ не будет содержать ссылки на фотографии - скрипт запросит ссылки на все имеющиеся фотографии в базе и вернет список, содержащий требуемое количество ссылок на фотографии (будут выбраны случайным образом из ответа API).

`-n` (number_of_photos) - количество публикуемых изображений. Необязательный параметр. По дефолту равен 1.

Пример команды:
```sh
python publish_random_photo.py -s spacex -n 3
```

#### `get_photos`

Вспомогательный скрипт. Содержит функции, необходимые для работы `photobot.py`. Ничего не возвращает при запуске.

Список функций:
 1. `get_directory_path(folder_name)` - проверяет наличие папки с названием `folder_name` в одной директории со скриптами и возвращает путь к ней.
 2. `compress_image(image_path, max_size_mb)` - сжимает сохраненное изображение, находящееся по ссылке `image_path`, если его размер в Мб превышает `max_size_mb` (default = 15)
 3. `find_images(folder_path)` - возвращает список путей к файлам форматов `.jpg, .jpeg, .png, .gif`, присутствующих в папке `folder_path`.
 4. `get_photos(folder_name)` - проверяет наличие папки `folder_name` с помощью `get_directory_path()`, после чего передает путь к `folder_name` функции `find_images()`. В случае если `find_images()` возвращает пустой список (т. е. в папке нет изображений), сообщает об этом, вызвав ошибку.


#### `save_photos`

Вспомогательный скрипт. Содержит функции, необходимые для работы `publish_random_photo`. Ничего не возвращает при запуске.

Список функций:
 1. `get_image_format(link)` - принимает на вход ссылку на файл и возвращает формат файла.
 2. `save_photos(links_listed, folder)` - скачивает изображения по ссылкам из списка `links_listed` и сохраняет их в папку `folder`, находящуюся в одной директории со скриптами. Если такой папки нет, автоматически создает ее.


#### `fetch_space_x_launch_photos.py`, `fetch_nasa_apod_photos.py`, `fetch_nasa_epic_photos.py`

Вспомогательные скрипты для `publish_random_photo`. Создают запрос к соответствующим API. После запуска сохранят изображения в папки с соответствующими названиями ('spacex', 'epic' и 'apod').

Каждый из скриптов можно запустить консольной командой, включающей следующие параметры:

 1. Для всех

`-n` (number_of_links) - число запрашиваемых ссылок. Необязательный параметр. По дефолту равен 1. 

 2. Только для `fetch_space_x_launch_photos.py`
    
`-l` (launch_id) - ID конкретного запуска при создании запроса к API SpaceX (str). Необязательный параметр. При отсутствии будет выполнен запрос фотографий с последнего запуска SpaceX. Если ответ на запрос не будет содержать ссылки на фотографии - скрипт запросит ссылки на все имеющиеся фотографии в базе, выберет случайным образом требуемое количество и сохранит.

 3. Только для  `fetch_nasa_apod_photos.py` и `fetch_nasa_epic_photos.py`

`-t` (nasa_api_token) - Токен NASA API (str). Необязательный параметр. Дефолтное значение - 'DEMO_KEY'. 
 
Пример команды:
```sh
python fetch_nasa_epic_photos.py -n 3 -t yournasaapitoken1234567890nasaapitoken01
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
