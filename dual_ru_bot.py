import os
import telebot
import logging
import json
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from dotenv import load_dotenv

# Настройка логирования для Better Stack
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Добавляем дополнительные поля для структурированного логирования
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'chat_id'):
            log_entry['chat_id'] = record.chat_id
        if hasattr(record, 'model'):
            log_entry['model'] = record.model
        if hasattr(record, 'message_length'):
            log_entry['message_length'] = record.message_length
            
        return json.dumps(log_entry, ensure_ascii=False)

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем форматтер
formatter = JSONFormatter()

# Файловый обработчик
file_handler = logging.FileHandler('bot.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Консольный обработчик
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Загружаем переменные окружения
load_dotenv()

# Импортируем наши вспомогательные функции
from gigachat_helper import get_giga_response
from yandex_gpt_helper import get_yandex_response

# Получаем токен для Telegram бота
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    logger.error("Не найден токен Telegram бота в переменных окружения")
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в переменных окружения")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Словарь для хранения текущей модели для каждого пользователя
user_modes = {}

def log_user_message(message, action="получено"):
    """Логирует сообщения пользователя в структурированном формате"""
    log_record = logging.LogRecord(
        name=__name__,
        level=logging.INFO,
        pathname=__file__,
        lineno=0,
        msg=f"Сообщение {action} | User ID: {message.from_user.id}, Username: @{message.from_user.username or 'N/A'}, Name: {message.from_user.first_name or 'N/A'} | Chat ID: {message.chat.id}, Type: {message.chat.type} | Текст: {message.text}",
        args=(),
        exc_info=None
    )
    log_record.user_id = message.from_user.id
    log_record.chat_id = message.chat.id
    log_record.message_length = len(message.text) if message.text else 0
    logger.handle(log_record)

def log_bot_response(chat_id, response, mode):
    """Логирует ответы бота в структурированном формате"""
    log_record = logging.LogRecord(
        name=__name__,
        level=logging.INFO,
        pathname=__file__,
        lineno=0,
        msg=f"Ответ бота отправлен | Chat ID: {chat_id} | Модель: {mode} | Длина ответа: {len(response)} символов",
        args=(),
        exc_info=None
    )
    log_record.chat_id = chat_id
    log_record.model = mode
    log_record.message_length = len(response)
    logger.handle(log_record)
    
    # Логируем первые 200 символов ответа для диагностики
    preview = response[:200] + "..." if len(response) > 200 else response
    logger.debug(f"Превью ответа: {preview}")

@bot.message_handler(commands=['start'])
def handle_start(message):
    """Обработчик команды /start"""
    log_user_message(message, "команда /start")
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("GigaChat", callback_data="giga"),
        InlineKeyboardButton("YandexGPT", callback_data="yandex")
    )
    
    response_text = "Выберите модель для общения:"
    bot.send_message(
        message.chat.id,
        response_text,
        reply_markup=markup
    )
    log_bot_response(message.chat.id, response_text, "menu")

@bot.message_handler(commands=['giga'])
def handle_giga(message):
    """Обработчик команды /giga"""
    log_user_message(message, "команда /giga")
    
    user_modes[message.chat.id] = "giga"
    response_text = "Режим переключен на GigaChat. Задавай свой вопрос."
    bot.send_message(message.chat.id, response_text)
    log_bot_response(message.chat.id, response_text, "giga")

@bot.message_handler(commands=['yandex'])
def handle_yandex(message):
    """Обработчик команды /yandex"""
    log_user_message(message, "команда /yandex")
    
    user_modes[message.chat.id] = "yandex"
    response_text = "Режим переключен на YandexGPT. Задавай свой вопрос."
    bot.send_message(message.chat.id, response_text)
    log_bot_response(message.chat.id, response_text, "yandex")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    """Обработчик нажатий на кнопки"""
    chat_id = call.message.chat.id
    user_info = f"User ID: {call.from_user.id}, Username: @{call.from_user.username or 'N/A'}"
    logger.info(f"Нажата кнопка | {user_info} | Chat ID: {chat_id} | Кнопка: {call.data}")
    
    if call.data == "giga":
        user_modes[chat_id] = "giga"
        bot.answer_callback_query(call.id)
        response_text = "Режим переключен на GigaChat. Задавай свой вопрос."
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=response_text
        )
        log_bot_response(chat_id, response_text, "giga")
    
    elif call.data == "yandex":
        user_modes[chat_id] = "yandex"
        bot.answer_callback_query(call.id)
        response_text = "Режим переключен на YandexGPT. Задавай свой вопрос."
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=response_text
        )
        log_bot_response(chat_id, response_text, "yandex")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обработчик текстовых сообщений"""
    chat_id = message.chat.id
    
    if chat_id not in user_modes:
        log_user_message(message, "без выбранной модели")
        handle_start(message)
        return
    
    mode = user_modes[chat_id]
    user_message = message.text
    
    log_user_message(message, f"для обработки моделью {mode}")
    
    try:
        logger.info(f"Отправка запроса к {mode} | Chat ID: {chat_id} | Длина запроса: {len(user_message)} символов")
        
        if mode == "giga":
            response = get_giga_response(user_message)
        else:  # yandex
            response = get_yandex_response(user_message)
        
        bot.send_message(chat_id, response)
        log_bot_response(chat_id, response, mode)
        
    except Exception as e:
        error_msg = f"Ошибка при обработке сообщения: {str(e)}"
        logger.error(error_msg)
        error_response = "Произошла ошибка при обработке запроса. Попробуйте позже."
        bot.send_message(chat_id, error_response)
        log_bot_response(chat_id, error_response, f"{mode}_error")

# Устанавливаем команды бота
bot.set_my_commands([
    BotCommand("start", "Показать меню выбора модели"),
    BotCommand("giga", "Переключиться на GigaChat"),
    BotCommand("yandex", "Переключиться на YandexGPT"),
])

if __name__ == "__main__":
    logger.info("Бот запущен")
    bot.polling(none_stop=True)