import requests
import random
import argparse
import save_photos


def get_random_photos(how_much) -> list:
    response = requests.get(
        'https://api.spacexdata.com/v5/launches', timeout=20)
    response.raise_for_status()
    response_data = response.json()
    launch_photos = []
    for launches in response_data:
        orig_launches_flickr_links = launches['links']['flickr']['original']
        if orig_launches_flickr_links:
            for link in orig_launches_flickr_links:
                launch_photos.append(link)
    random_photos = random.sample(launch_photos, how_much)
    return random_photos


def get_spacex_photo_links(launch_id: str = None, how_much: int = 1) -> list:
    if not launch_id:
        response = requests.get(
            'https://api.spacexdata.com/v5/launches/latest', timeout=20)
        response.raise_for_status()
        response_data = response.json()['links']['flickr']['original']
        if not response_data:
            return get_random_photos(how_much)
        return response_data
    else:
        params = {'id': launch_id}
        response = requests.get(
            'https://api.spacexdata.com/v5/launches/',
            params=params,
            timeout=20
        )
        response.raise_for_status()
        return response.json()['links']['flickr']['original']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n',
                        '--number_of_links',
                        help='Количество ссылок на изображения',
                        type=int,
                        default=1,
                        )
    parser.add_argument('-l', '--launch_id',
                        help='ID запуска', type=str, default='')
    args = parser.parse_args()
    number_of_links = args.number_of_links
    launch_id = args.launch_id
    links = get_spacex_photo_links(launch_id, number_of_links)
    save_photos.save_photos(links, 'spacex')


if __name__ == '__main__':
    main()
