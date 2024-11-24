import os
import random
import argparse
from dotenv import load_dotenv
import telegram
import fetch_nasa_apod_photos
import fetch_space_x_launch_photos
import fetch_nasa_epic_photos


load_dotenv('env.env')
BOT_TOKEN = os.getenv('bot_token')
GROUP_ID = os.getenv('tg_group_id')


def main():
    sources = ['spacex', 'epic', 'apod']
    random_source = random.choice(sources)
    parser = argparse.ArgumentParser(
        description='Публикация фото в Telegram канал'
    )
    parser.add_argument('-s', '--source', choices=sources,
                        default=random_source, help='Источник фото')
    parser.add_argument('-n', '--number_of_photos',
                        help='Количество изображений', type=int, default=1)
    parser.add_argument('-l', '--launch_id', help='ID запуска, только для SpaceX', type=int)
    args = parser.parse_args()
    number_of_photos = args.number_of_photos

    bot = telegram.Bot(BOT_TOKEN)

    links_list = []

    if args.source == 'spacex':
        
        links_list = fetch_space_x_launch_photos.main(
            launch_id=args.launch_id, how_much=number_of_photos)
    elif args.source == 'epic':
        links_list = fetch_nasa_epic_photos.main(how_much=number_of_photos)
    elif args.source == 'apod':
        links_list = fetch_nasa_apod_photos.main(how_much=number_of_photos)

    for link in links_list:
        bot.send_photo(chat_id=GROUP_ID, photo=link)


if __name__ == '__main__':
    main()
