import requests
import random


def random_photos(how_much) -> list:
    response = requests.get(
        'https://api.spacexdata.com/v5/launches', timeout=20)
    response.raise_for_status()
    response_data = response.json()
    launch_photos = []
    for launches in response_data:
        if launches['links']['flickr']['original']:
            for link in launches['links']['flickr']['original']:
                launch_photos.append(link)
    random_photos = random.sample(launch_photos, how_much)
    return random_photos


def main(launch_id: str = None, how_much: int = 1) -> list:
    if not launch_id:
        response = requests.get(
            'https://api.spacexdata.com/v5/launches/latest', timeout=20)
        response.raise_for_status()
        response_data = response.json()['links']['flickr']['original']
        if not response_data:
            return random_photos(how_much) 
        return response_data       
    else:
        params = {'id': launch_id}
        response = requests.get(
            'https://api.spacexdata.com/v5/launches/', params=params, timeout=20)
        response.raise_for_status()
        return response.json()['links']['flickr']['original']


if __name__ == '__main__':
    main()
