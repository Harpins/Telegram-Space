import os
from dotenv import load_dotenv
import requests

load_dotenv('env.env')
NASA_API_TOKEN = os.getenv('nasa_token')

def main(how_much:int=1) -> list:
    parameters = {
        'count': how_much,
        'api_key': NASA_API_TOKEN,
    } 
    response = requests.get('https://api.nasa.gov/planetary/apod', params = parameters,  timeout=20)
    response.raise_for_status()
    response_data = response.json()
    nasa_photos_links = []
    for photos_data in response_data:
        nasa_photos_links.append(photos_data['url'])
    return nasa_photos_links

if __name__ == '__main__':
    main()