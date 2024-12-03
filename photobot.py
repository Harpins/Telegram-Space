import os
import random
import time
import tempfile
import shutil
import argparse
from dotenv import load_dotenv
import telegram
from get_photos import get_photos, compress_image


def send_photo_with_bot(bot_token: str, group_id: str, time_interval_h: int, photo_paths: list) -> None:
    sleep_time = time_interval_h*3600
    bot = telegram.Bot(bot_token)
    while photo_paths:
        for path in photo_paths:
            with open(f'{path}', 'rb') as photo:
                bot.send_photo(chat_id=group_id, photo=photo)
                time.sleep(1)
        time.sleep(sleep_time)
    return


def main():
    load_dotenv('env.env')
    bot_token = os.environ['TG_BOT_TOKEN']
    group_id = os.environ['TG_GROUP_ID']
    time_interval_h = int(os.getenv('TIME_INTERVAL_H', default='4'))

    parser = argparse.ArgumentParser(
        description='Введите название директории и сколько изображений публиковать'
    )
    parser.add_argument('-f', '--folder_name', required=True,
                        help='Название директории с изображениями', type=str)
    parser.add_argument('-n', '--number_of_photos',
                        help='Количество изображений', type=int, default=1)
    args = parser.parse_args()
    if args.number_of_photos < 1:
        raise ValueError('Количество изображений должно быть более 1')

    folder_name = args.folder_name
    number_of_photos = args.number_of_photos

    photo_paths = get_photos(folder_name=folder_name)

    tempphoto_paths = []
    with tempfile.TemporaryDirectory() as tempdir:
        for path in photo_paths:
            temp_file_path = os.path.join(tempdir, os.path.basename(path))
            shutil.copy2(path, temp_file_path)
            compress_image(temp_file_path)
            tempphoto_paths.append(temp_file_path)

        random.shuffle(tempphoto_paths)

        if len(tempphoto_paths) < number_of_photos:
            raise ValueError(
                f'В папке {folder_name} менее {number_of_photos} изображений'
                )
        elif len(tempphoto_paths) > number_of_photos:
            tempphoto_paths = tempphoto_paths[:number_of_photos]

        try:
            send_photo_with_bot(bot_token, group_id,
                                time_interval_h, tempphoto_paths)
        except telegram.error.NetworkError:
            print('Переподключаемся')
            attempt = 0
            while attempt < 5:
                try:
                    send_photo_with_bot(bot_token, group_id,
                                        time_interval_h, tempphoto_paths)
                    break
                except telegram.error.NetworkError:
                    attempt += 1
                    print('Не удалось подключиться, пробуем снова')
                    time.sleep(5)
            print('Соединение разорвано')
            return
        except telegram.error.RetryAfter as error:
            print(f'Повтор запроса через {error.retry_after} секунд')
            time.sleep(error.retry_after)
            send_photo_with_bot(bot_token, group_id,
                                time_interval_h, tempphoto_paths)


if __name__ == '__main__':
    main()
