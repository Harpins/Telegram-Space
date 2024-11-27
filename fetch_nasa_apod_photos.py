import os
from dotenv import load_dotenv
import requests
import argparse
import pprint


def get_links_list(how_much: int = 1) -> list:
    load_dotenv('env.env')
    nasa_api_token = os.getenv('NASA_TOKEN', 'DEMO_KEY')
    parameters = {
        'count': how_much,
        'api_key': nasa_api_token,
    }
    response = requests.get(
        'https://api.nasa.gov/planetary/apod', params=parameters,  timeout=20)
    response.raise_for_status()
    response_data = response.json()
    nasa_photos_links = []
    for media_data in response_data:
        if 'media_type' in media_data and media_data['media_type'] == 'image':
            nasa_photos_links.append(media_data['url'])
    return nasa_photos_links


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number_of_links',
                        help='Количество ссылок на изображения', type=int, default=1)
    args = parser.parse_args()
    number_of_links = args.number_of_links
    pprint.pprint(get_links_list(number_of_links))


if __name__ == '__main__':
    main()
