import pytest
from main import get_random_cat_image
import requests
import logging

# Настройка логирования для тестов
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Тест для успешного запроса к API
def test_get_random_cat_image_success(mocker):
    """
    Тестирует успешный запрос к API и проверяет, что функция возвращает правильный URL.
    """
    # Мокируем метод requests.get в модуле main
    mock_get = mocker.patch('main.requests.get')

    # Настраиваем объект ответа
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    # Настраиваем метод raise_for_status() так, чтобы он не делал ничего при статусе 200
    mock_response.raise_for_status = lambda: None
    # Задаём возвращаемое значение для метода json()
    mock_response.json.return_value = [
        {
            'id': 'abc123',
            'url': 'https://cdn2.thecatapi.com/images/abc123.jpg',
            'width': 500,
            'height': 375
        }
    ]

    # Вызываем функцию и проверяем результат
    image_url = get_random_cat_image()
    assert image_url == 'https://cdn2.thecatapi.com/images/abc123.jpg'
    logger.info("Тест успешного запроса пройден успешно")

# Тест для неуспешного запроса к API
def test_get_random_cat_image_failure(mocker):
    """
    Тестирует неуспешный запрос к API (например, статус код 404) и проверяет, что функция возвращает None.
    """
    # Мокируем метод requests.get в модуле main
    mock_get = mocker.patch('main.requests.get')

    # Настраиваем объект ответа с кодом состояния 404
    mock_response = mock_get.return_value
    mock_response.status_code = 404
    # Настраиваем метод raise_for_status() для генерации исключения HTTPError
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
    # Предотвращаем вызов метода json(), т.к. он не должен вызываться при ошибке
    mock_response.json = mocker.Mock()

    # Вызываем функцию и проверяем результат
    image_url = get_random_cat_image()
    assert image_url is None
    logger.info("Тест неуспешного запроса пройден успешно")

    # Проверяем, что метод json() не был вызван
    mock_response.json.assert_not_called()

# Тест для обработки исключения
def test_get_random_cat_image_exception(mocker):
    """
    Тестирует обработку исключения при выполнении запроса (например, таймаут соединения).
    """
    # Мокируем метод requests.get так, чтобы он вызывал исключение Timeout
    mock_get = mocker.patch('main.requests.get', side_effect=requests.exceptions.Timeout("Connection timed out"))

    # Вызываем функцию и проверяем результат
    image_url = get_random_cat_image()
    assert image_url is None
    logger.info("Тест обработки исключения пройден успешно")
