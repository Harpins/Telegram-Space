import os
from dotenv import load_dotenv
import requests
import argparse
import pprint
from datetime import datetime


def get_links_list(how_much: int = 1) -> list:
    load_dotenv('env.env')
    nasa_api_token = os.getenv('NASA_TOKEN', 'DEMO_KEY')
    parameters = {
        'api_key': nasa_api_token,
    }
    response = requests.get(
        'https://api.nasa.gov/EPIC/api/natural/images', params=parameters,  timeout=20)
    response.raise_for_status()
    response_data = response.json()
    links_list = []
    for instance in range(how_much):
        response_data_example = response_data[instance]
        datetime_object = datetime.strptime(
            response_data_example['date'], '%Y-%m-%d %H:%M:%S')
        image_date = datetime_object.strftime('%Y/%m/%d')
        image = response_data_example['image']
        link = f'https://epic.gsfc.nasa.gov/archive/natural/{
            image_date}/png/{image}.png'
        response = requests.get(link,  timeout=20)
        response.raise_for_status()
        links_list.append(link)
    return links_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number_of_links',
                        help='Количество ссылок на изображения', type=int, default=1)
    args = parser.parse_args()
    number_of_links = args.number_of_links
    pprint.pprint(get_links_list(number_of_links))


if __name__ == '__main__':
    main()
