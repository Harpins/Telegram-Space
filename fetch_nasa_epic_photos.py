import requests
import argparse
from datetime import datetime
import save_photos


def get_nasa_epic_photo_links(how_much: int = 1, nasa_token: str = 'DEMO_KEY') -> list:
    parameters = {
        'api_key': nasa_token,
    }
    response = requests.get(
        'https://api.nasa.gov/EPIC/api/natural/images', params=parameters,  timeout=20)
    response.raise_for_status()
    response_data = response.json()
    links = []
    for instance in range(how_much):
        response_data_example = response_data[instance]
        datetime_object = datetime.strptime(
            response_data_example['date'], '%Y-%m-%d %H:%M:%S')
        image_date = datetime_object.strftime('%Y/%m/%d')
        image = response_data_example['image']
        link = f'https://epic.gsfc.nasa.gov/archive/natural/{image_date}/png/{image}.png'
        response = requests.get(link,  timeout=20)
        response.raise_for_status()
        links.append(link)
    
    return links


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number_of_links',
                        help='Количество ссылок на изображения', type=int, default=1)
    parser.add_argument('-t', '--nasa_api_token', 
                        help='Токен NASA API', type=str, default='DEMO_KEY')
    args = parser.parse_args()
    number_of_links = args.number_of_links
    nasa_token = args.nasa_api_token
    links = get_nasa_epic_photo_links(number_of_links, nasa_token)
    save_photos.save_photos(links, 'epic') 


if __name__ == '__main__':
    main()
