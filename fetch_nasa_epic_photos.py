import requests

def main(how_much:int=1) -> list:
    parameters = {
        'api_key': 'DEMO_KEY',
    } 
    response = requests.get('https://api.nasa.gov/EPIC/api/natural/images', params = parameters,  timeout=20)
    response.raise_for_status()
    response_data = response.json()
    links_list = []
    instance = 0
    while instance < how_much:
        response_data_example = response_data[instance]
        example_date = response_data_example['date'][:10].split('-')
        image = response_data_example['image']
        year = example_date[0]
        month = example_date[1]
        day = example_date[2]
        link = f'https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/png/{image}.png'
        response = requests.get(link,  timeout=20)
        response.raise_for_status()
        links_list.append(link)
        instance+=1
    return links_list

if __name__ == '__main__':
    main()