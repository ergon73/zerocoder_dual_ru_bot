import pytest
from unittest.mock import patch, MagicMock
from dual_ru_bot import bot

def test_start_command():
    """Тест проверяет обработку команды /start"""
    message = MagicMock()
    message.chat.id = 12345
    message.text = "/start"

    with patch.object(bot, 'send_message') as mock_send:
        # Находим нужный обработчик и вызываем его
        for handler in bot.message_handlers:
            if 'commands' in handler['filters'] and 'start' in handler['filters']['commands']:
                handler['function'](message)
                break
        
        mock_send.assert_called_once()
        args = mock_send.call_args[0]
        assert args[0] == 12345  # chat_id
        assert "Выберите модель" in args[1]  # message text

def test_giga_command():
    """Тест проверяет обработку команды /giga"""
    message = MagicMock()
    message.chat.id = 12345
    message.text = "/giga"

    with patch.object(bot, 'send_message') as mock_send:
        # Находим нужный обработчик и вызываем его
        for handler in bot.message_handlers:
            if 'commands' in handler['filters'] and 'giga' in handler['filters']['commands']:
                handler['function'](message)
                break
        
        mock_send.assert_called_once()
        args = mock_send.call_args[0]
        assert args[0] == 12345
        assert "GigaChat" in args[1]

def test_yandex_command():
    """Тест проверяет обработку команды /yandex"""
    message = MagicMock()
    message.chat.id = 12345
    message.text = "/yandex"

    with patch.object(bot, 'send_message') as mock_send:
        # Находим нужный обработчик и вызываем его
        for handler in bot.message_handlers:
            if 'commands' in handler['filters'] and 'yandex' in handler['filters']['commands']:
                handler['function'](message)
                break
        
        mock_send.assert_called_once()
        args = mock_send.call_args[0]
        assert args[0] == 12345
        assert "YandexGPT" in args[1] 