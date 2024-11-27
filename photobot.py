import os
import random
import time
import argparse
from dotenv import load_dotenv
import telegram
import get_photos


load_dotenv('env.env')
BOT_TOKEN = os.getenv('bot_token')
GROUP_ID = os.getenv('tg_group_id')
TIME_INTERVAL_H = int(os.getenv('time_interval_h'))


def main():
    parser = argparse.ArgumentParser(
        description='Введите название директории и сколько изображений публиковать'
    )
    parser.add_argument(
        'folder_name', help='Название директории с изображениями', type=str)
    parser.add_argument('number_of_photos',
                        help='Количество изображений', type=int)
    args = parser.parse_args()
    folder_name = args.folder_name
    number_of_photos = args.number_of_photos
    sleep_time = TIME_INTERVAL_H*3600
    bot = telegram.Bot(BOT_TOKEN)
    photo_paths = get_photos.main(folder_name=folder_name)
    random.shuffle(photo_paths)
    if len(photo_paths) < number_of_photos:
        raise Exception(f'В папке {folder_name} менее {number_of_photos} изображений')
    elif len(photo_paths) > number_of_photos:
        photo_paths = photo_paths[:number_of_photos]
    while photo_paths:
        for path in photo_paths:
            with open(f'{path}', 'rb') as photo:
                bot.send_photo(chat_id=GROUP_ID, photo=photo)
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
