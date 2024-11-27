import os
import math
import requests
from urllib.parse import urlparse


def get_image_format(link: str) -> str:
    parsed_url = urlparse(link)
    if not parsed_url.scheme:
        link = f'http://{link}'
        parsed_url = urlparse(link)
    return parsed_url.path.split('.')[-1]


def save_photos(links_listed: list = None, folder: str = 'images') -> None:
    if not links_listed:
        raise ValueError('Список ссылок не был передан')
    os.makedirs(folder, exist_ok=True)
    for link in links_listed:
        image_format = get_image_format(link)
        image_name = str(links_listed.index(link)).zfill(
            int(math.ceil(math.log10(len(links_listed)))))
        image_path = os.path.join(folder, image_name)
        with open(f'{image_path}.{image_format}', 'wb') as image:
            response = requests.get(link, timeout=20)
            response.raise_for_status()
            image.write(response.content)


def main():
    return


if __name__ == '__main__':
    main()
