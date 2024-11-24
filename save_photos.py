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


def main(link_list: list[str] = [], folder: str = 'images') -> None:
    if not link_list:
        raise Exception('Список ссылок не был передан')
    if not os.path.exists(folder):
        os.makedirs(folder)
    for link in link_list:
        image_format = get_image_format(link)
        image_name = str(link_list.index(link)).zfill(
            int(math.ceil(math.log10(len(link_list)))))
        with open(f'{folder}/{image_name}.{image_format}', 'wb') as image:
            response = requests.get(link, timeout=20)
            response.raise_for_status()
            image.write(response.content)


if __name__ == '__main__':
    main()
