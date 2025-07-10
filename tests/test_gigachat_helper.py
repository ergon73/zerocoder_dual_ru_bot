import os
import pytest
from unittest.mock import patch, MagicMock
from gigachat_helper import get_giga_response

def test_get_giga_response_no_credentials():
    """Тест проверяет поведение функции при отсутствии учетных данных"""
    with patch.dict(os.environ, {}, clear=True):
        response = get_giga_response("Test prompt")
        assert "Не удалось получить ответ от GigaChat" in response

def test_get_giga_response_success():
    """Тест проверяет успешный запрос к API"""
    # Создаем мок для ответа
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="Test response"))
    ]

    # Создаем мок для GigaChat
    mock_gigachat_instance = MagicMock()
    mock_gigachat_instance.chat.return_value = mock_response
    mock_gigachat_class = MagicMock(return_value=mock_gigachat_instance)

    with patch.dict(os.environ, {
        "GIGACHAT_CREDENTIALS": "test-creds",
        "GIGACHAT_CERT_PATH": "test-cert.cer"
    }), patch('os.path.exists', return_value=True), patch('gigachat_helper.GigaChat', mock_gigachat_class):
        response = get_giga_response("Test prompt")
        assert response == "Test response"
        mock_gigachat_instance.chat.assert_called_once()

def test_get_giga_response_api_error():
    """Тест проверяет обработку ошибки API"""
    # Создаем мок для GigaChat
    mock_gigachat_instance = MagicMock()
    mock_gigachat_instance.chat.side_effect = Exception("API Error")
    mock_gigachat_class = MagicMock(return_value=mock_gigachat_instance)

    with patch.dict(os.environ, {
        "GIGACHAT_CREDENTIALS": "test-creds",
        "GIGACHAT_CERT_PATH": "test-cert.cer"
    }), patch('os.path.exists', return_value=True), patch('gigachat_helper.GigaChat', mock_gigachat_class):
        response = get_giga_response("Test prompt")
        assert "Не удалось получить ответ от GigaChat" in response
        mock_gigachat_instance.chat.assert_called_once() 