import requests
import argparse
import save_photos


def get_nasa_apod_photo_links(how_much: int = 1, nasa_token: str = 'DEMO_KEY') -> list:
    parameters = {
        'count': how_much,
        'api_key': nasa_token,
    }
    response = requests.get(
        'https://api.nasa.gov/planetary/apod', params=parameters,  timeout=20)
    response.raise_for_status()
    response_data = response.json()
    links = []
    for media_data in response_data:
        if 'media_type' in media_data and media_data['media_type'] == 'image':
            links.append(media_data['url']) 
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
    links = get_nasa_apod_photo_links(number_of_links, nasa_token)  
    save_photos.save_photos(links, 'apod')     
    

if __name__ == '__main__':
    main()
