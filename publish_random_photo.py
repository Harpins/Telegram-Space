import os
import random
from time import sleep
import argparse
from dotenv import load_dotenv
import telegram
import fetch_nasa_apod_photos
import fetch_space_x_launch_photos
import fetch_nasa_epic_photos
import save_photos

def main():
    load_dotenv('env.env')
    bot_token = os.environ['TG_BOT_TOKEN']
    group_id = os.environ['TG_GROUP_ID']
    nasa_token = os.getenv('NASA_TOKEN', default = 'DEMO_KEY')
    sources = ['spacex', 'epic', 'apod']
    random_source = random.choice(sources)
    parser = argparse.ArgumentParser(
        description='Публикация фото в Telegram канал'
    )
    parser.add_argument('-s', '--source', choices=sources,
                        default=random_source, help='Источник фото')
    parser.add_argument('-n', '--number_of_photos',
                        help='Количество изображений', type=int, default=1)
    parser.add_argument('-l', '--launch_id',
                        help='ID запуска, только для SpaceX', type=int)
    args = parser.parse_args()
    number_of_photos = args.number_of_photos

    bot = telegram.Bot(bot_token)

    links_listed = []

    if args.source == 'spacex':
        links_listed = fetch_space_x_launch_photos.get_spacex_photo_links(
            launch_id=args.launch_id, how_much=number_of_photos)
        save_photos.save_photos(links_listed, 'spacex') 
    elif args.source == 'epic':
        links_listed = fetch_nasa_epic_photos.get_nasa_epic_photo_links(
            how_much=number_of_photos, nasa_token=nasa_token)
        save_photos.save_photos(links_listed, 'epic') 
    elif args.source == 'apod':
        links_listed = fetch_nasa_apod_photos.get_nasa_apod_photo_links(
            how_much=number_of_photos, nasa_token=nasa_token)
        save_photos.save_photos(links_listed, 'apod') 
        

    for link in links_listed:
        bot.send_photo(chat_id=group_id, photo=link)
        sleep(1)


if __name__ == '__main__':
    main()
