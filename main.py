import requests

def get_random_cat_image():
    url = 'https://api.thecatapi.com/v1/images/search'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем на наличие HTTP ошибок
        data = response.json()
        if data:
            return data[0]['url']
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
