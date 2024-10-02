import pytest
from main import get_random_cat_image
import requests

def test_get_random_cat_image_success(mocker):
    mock_get = mocker.patch('main.requests.get')
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.raise_for_status = lambda: None  # Не делает ничего, если статус 200
    mock_response.json.return_value = [
        {
            'id': 'abc123',
            'url': 'https://cdn2.thecatapi.com/images/abc123.jpg',
            'width': 500,
            'height': 375
        }
    ]

    image_url = get_random_cat_image()
    assert image_url == 'https://cdn2.thecatapi.com/images/abc123.jpg'

def test_get_random_cat_image_failure(mocker):
    mock_get = mocker.patch('main.requests.get')
    mock_response = mock_get.return_value
    mock_response.status_code = 404
    # Настраиваем raise_for_status() для генерации HTTPError
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
    # Убеждаемся, что response.json() не будет вызван
    mock_response.json = mocker.Mock()

    image_url = get_random_cat_image()
    assert image_url is None
    # Проверяем, что response.json() не был вызван
    mock_response.json.assert_not_called()

def test_get_random_cat_image_exception(mocker):
    # Моделируем исключение при выполнении requests.get()
    mock_get = mocker.patch('main.requests.get', side_effect=requests.exceptions.Timeout("Connection timed out"))

    image_url = get_random_cat_image()
    assert image_url is None
