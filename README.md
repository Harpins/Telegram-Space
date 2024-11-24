# Космический Телеграм

Набор скриптов для публикации фото в Telegram-канал

Основные скрипты
- `photobot.py`
Позволяет автоматически публиковать в Telegram-канал фото из папки, находящейся в одном репозитории со скриптом с периодичностью (в ч), устанавливаемой в переменных окружения.
Вспомогательный скрипт - `get_photos.py`
- `publish_random_photo`
Позволяет опубликовать в Telegram-канал одно или несколько фото по запросу к: 
    1. [API SpaceX](https://github.com/r-spacex/SpaceX-API)
   
       Вспомогательный скрипт - `fetch_space_x_launch_photos.py`
   
    2. [NASA API APOD](https://github.com/nasa/apod-api)
   
       Вспомогательный скрипт - `fetch_nasa_apod_photos.py`
   
    3. [NASA API EPIC](https://epic.gsfc.nasa.gov/about/epic)
   
       Вспомогательный скрипт - `fetch_nasa_epic_photos.py`

  Также сохраняет опубликованные изображения в папки с соответствующим названием. Вспомогательный скрипт - `save_photos.py`

### Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `env.env` рядом со скриптами и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 4 переменные:
- Используемые в основных скриптах
  
  `BOT_TOKEN` - [Токен Telegram бота](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)
  
  `TG_GROUP_ID` - [ID группы Telegram](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)

- Используемая в `fetch_nasa_apod_photos.py`
  
  `NASA_TOKEN` - [Токен NASA API](https://api.nasa.gov/)

- Используемая для задания периодичности публикации (в ч) в `photobot.py`
  
  `TIME_INTERVAL_H` 


### Как установить

Скачайте репозиторий целиком.

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Как запустить

- `photobot.py`
 
Запустите скрипт командой, включающей название папки, из которой будут публиковаться изображения (наличие папки в одной директории со скриптом обязательно) и количество публикуемых за раз изображений из данной папки (необязательный параметр, default = 1).
Пример команды:
```sh
python photobot.py yourfolder 2
```

- `publish_random_photo`
  
Запустите скрипт консольной командой.

Команда может включать следующие параметры:

`-s` (source) выбрать из списка `['spacex', 'epic', 'apod']` - выбор API для запроса ссылок на изображения. Необязательный параметр. По дефолту выбирается случайно из списка.
`-l` (launch_id) - ID конкретного запуска при создании запроса к API SpaceX. Необязательный параметр. При отсутствии будет выполнен запрос фотографии(-й) с последнего запуска SpaceX. В обоих случаях, если ответ не будет содержать ссылки на фотографии - скрипт запросит ссылки на все имеющиеся фотографии в базе и вернет список, содержащий требуемое количество ссылок (будут выбраны случайным образом) на фотографии.
`-n` (number_of_photos) - число запрашиваемых ссылок. Необязательный параметр. По дефолту равен 1.

Пример команды:
```sh
python publish_random_photo.py -s spacex -n 3
```
После запуска скрипт запросит список ссылок на фотографии, с помощью бота опубликует фото в Telegram-канале, скачает и сохранит изображения в папке, автоматически создаваемой в репозитории.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
