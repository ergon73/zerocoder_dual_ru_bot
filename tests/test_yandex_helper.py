import os
import pytest
from unittest.mock import patch, MagicMock
from yandex_gpt_helper import get_yandex_response

def test_get_yandex_response_no_credentials():
    """Тест проверяет поведение функции при отсутствии учетных данных"""
    with patch.dict(os.environ, {}, clear=True):
        response = get_yandex_response("Test prompt")
        assert "Ошибка конфигурации YandexGPT" in response

def test_get_yandex_response_success():
    """Тест проверяет успешный запрос к API"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": {
            "alternatives": [
                {
                    "message": {
                        "text": "Test response"
                    }
                }
            ]
        }
    }

    with patch.dict(os.environ, {
        "YANDEX_FOLDER_ID": "test-folder",
        "YANDEX_API_KEY": "test-key"
    }), patch('requests.post', return_value=mock_response):
        response = get_yandex_response("Test prompt")
        assert response == "Test response"

def test_get_yandex_response_api_error():
    """Тест проверяет обработку ошибки API"""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Error message"
    mock_response.json.return_value = {
        "error": {
            "message": "Test error"
        }
    }

    with patch.dict(os.environ, {
        "YANDEX_FOLDER_ID": "test-folder",
        "YANDEX_API_KEY": "test-key"
    }), patch('requests.post', return_value=mock_response):
        response = get_yandex_response("Test prompt")
        assert "Не удалось получить ответ от YandexGPT" in response 