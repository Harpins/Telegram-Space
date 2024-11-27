import os
import random
import time
import argparse
from dotenv import load_dotenv
import telegram
from get_photos import get_photos, compress_image


def main():
    load_dotenv('env.env')
    bot_token = os.getenv('BOT_TOKEN')
    group_id = os.getenv('TG_GROUP_ID')
    time_interval_h = int(os.getenv('TIME_INTERVAL_H'))
    parser = argparse.ArgumentParser(
        description='Введите название директории и сколько изображений публиковать'
    )
    parser.add_argument('-f', '--folder_name', required=True,
                        help='Название директории с изображениями', type=str)
    parser.add_argument('-n', '--number_of_photos',
                        help='Количество изображений', type=int, default=1)
    args = parser.parse_args()
    folder_name = args.folder_name
    number_of_photos = args.number_of_photos
    sleep_time = time_interval_h*3600
    bot = telegram.Bot(bot_token)
    photo_paths = get_photos(folder_name=folder_name)
    for path in photo_paths:
        compress_image(path)
    random.shuffle(photo_paths)
    if len(photo_paths) < number_of_photos:
        raise ValueError(
            f'В папке {folder_name} менее {number_of_photos} изображений'
        )
    elif len(photo_paths) > number_of_photos:
        photo_paths = photo_paths[:number_of_photos]
    while photo_paths:
        for path in photo_paths:
            with open(f'{path}', 'rb') as photo:
                bot.send_photo(chat_id=group_id, photo=photo)
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
