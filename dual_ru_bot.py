import os
import telebot
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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

@bot.message_handler(commands=['start'])
def handle_start(message):
    """Обработчик команды /start"""
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("GigaChat", callback_data="giga"),
        InlineKeyboardButton("YandexGPT", callback_data="yandex")
    )
    bot.send_message(
        message.chat.id,
        "Выберите модель для общения:",
        reply_markup=markup
    )

@bot.message_handler(commands=['giga'])
def handle_giga(message):
    """Обработчик команды /giga"""
    user_modes[message.chat.id] = "giga"
    bot.send_message(
        message.chat.id,
        "Режим переключен на GigaChat. Задавай свой вопрос."
    )

@bot.message_handler(commands=['yandex'])
def handle_yandex(message):
    """Обработчик команды /yandex"""
    user_modes[message.chat.id] = "yandex"
    bot.send_message(
        message.chat.id,
        "Режим переключен на YandexGPT. Задавай свой вопрос."
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    """Обработчик нажатий на кнопки"""
    chat_id = call.message.chat.id
    
    if call.data == "giga":
        user_modes[chat_id] = "giga"
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text="Режим переключен на GigaChat. Задавай свой вопрос."
        )
    
    elif call.data == "yandex":
        user_modes[chat_id] = "yandex"
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text="Режим переключен на YandexGPT. Задавай свой вопрос."
        )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обработчик текстовых сообщений"""
    chat_id = message.chat.id
    
    if chat_id not in user_modes:
        handle_start(message)
        return
    
    mode = user_modes[chat_id]
    user_message = message.text
    
    try:
        if mode == "giga":
            response = get_giga_response(user_message)
        else:  # yandex
            response = get_yandex_response(user_message)
        
        bot.send_message(chat_id, response)
        
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {str(e)}")
        bot.send_message(
            chat_id,
            "Произошла ошибка при обработке запроса. Попробуйте позже."
        )

# Устанавливаем команды бота
bot.set_my_commands([
    BotCommand("start", "Показать меню выбора модели"),
    BotCommand("giga", "Переключиться на GigaChat"),
    BotCommand("yandex", "Переключиться на YandexGPT"),
])

if __name__ == "__main__":
    logger.info("Бот запущен")
    bot.polling(none_stop=True)