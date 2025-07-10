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

# Загружаем переменные окружения из .env файла
logger.info("Загрузка переменных окружения из .env файла")
load_dotenv()

# Проверяем наличие всех необходимых переменных
env_vars = {
    "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
    "YANDEX_FOLDER_ID": os.getenv("YANDEX_FOLDER_ID"),
    "YANDEX_API_KEY": os.getenv("YANDEX_API_KEY"),
    "GIGACHAT_CREDENTIALS": os.getenv("GIGACHAT_CREDENTIALS"),
    "GIGACHAT_CERT_PATH": os.getenv("GIGACHAT_CERT_PATH")
}

for var_name, value in env_vars.items():
    if value:
        # Маскируем токены в логах для безопасности
        masked_value = value[:6] + "..." + value[-4:] if len(value) > 10 else "***"
        logger.info(f"Загружена переменная {var_name}: {masked_value}")
    else:
        logger.warning(f"Переменная {var_name} не найдена в .env файле")

# Импортируем наши вспомогательные функции
from gigachat_helper import get_giga_response
from yandex_gpt_helper import get_yandex_response

# Получаем токен для Telegram бота
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    logger.error("Не найден токен Telegram бота в переменных окружения")
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в переменных окружения")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Устанавливаем команды бота
bot.set_my_commands([
    BotCommand("start", "Показать меню выбора модели"),
    BotCommand("giga", "Переключиться на GigaChat"),
    BotCommand("yandex", "Переключиться на YandexGPT"),
])

# Словарь для хранения текущей модели для каждого пользователя
user_modes = {}

# --- UI Кнопки ---
def create_model_choice_keyboard():
    """Создает клавиатуру с кнопками выбора модели."""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("🤖 GigaChat", callback_data="giga"),
        InlineKeyboardButton("🧠 YandexGPT", callback_data="yandex")
    )
    return keyboard

# --- Обработчики команд ---

@bot.message_handler(commands=['giga'])
def switch_to_giga(message):
    """Быстрое переключение на GigaChat."""
    user_id = message.from_user.id
    user_modes[user_id] = "giga"
    bot.reply_to(message, "Режим переключен на GigaChat. Задавай свой вопрос.")

@bot.message_handler(commands=['yandex'])
def switch_to_yandex(message):
    """Быстрое переключение на YandexGPT."""
    user_id = message.from_user.id
    user_modes[user_id] = "yandex"
    bot.reply_to(message, "Режим переключен на YandexGPT. Задавай свой вопрос.")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Отправляет приветственное сообщение и кнопки выбора модели."""
    welcome_text = "Привет! Я твой личный помощник. Выбери модель, с которой хочешь пообщаться:"
    bot.send_message(message.chat.id, welcome_text, reply_markup=create_model_choice_keyboard())

@bot.callback_query_handler(func=lambda call: call.data in ["giga", "yandex"])
def handle_model_choice(call):
    """Обрабатывает нажатие на кнопки выбора модели."""
    user_id = call.from_user.id
    chosen_model = call.data
    
    user_modes[user_id] = chosen_model
    model_name = "GigaChat" if chosen_model == "giga" else "YandexGPT"
    
    # Отправляем подтверждение пользователю
    bot.answer_callback_query(call.id, f"Режим переключен на {model_name}")
    bot.send_message(call.message.chat.id, f"Отлично! Теперь я отвечаю с помощью {model_name}. Задавай свой вопрос.")
    
    # Редактируем исходное сообщение, чтобы убрать кнопки
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обрабатывает текстовые сообщения пользователя."""
    user_id = message.from_user.id
    
    # Проверяем, выбрал ли пользователь модель
    if user_id not in user_modes:
        bot.send_message(message.chat.id, "Пожалуйста, сначала выбери модель с помощью команды /start")
        return

    # [cite_start]Показываем статус "Печатает..." для лучшего UX [cite: 140]
    bot.send_chat_action(message.chat.id, 'typing')
    
    user_prompt = message.text
    model = user_modes[user_id]
    
    response_text = ""
    parse_mode = None # По умолчанию без форматирования
    
    if model == "giga":
        response_text = get_giga_response(user_prompt)
        # [cite_start]GigaChat использует Markdown, как было выяснено в уроке [cite: 137, 143]
        # Для корректной работы Markdown в pyTelegramBotAPI лучше использовать 'MarkdownV2'
        parse_mode = 'MarkdownV2' 
    elif model == "yandex":
        response_text = get_yandex_response(user_prompt)

    # Важно: нужно экранировать символы для MarkdownV2, которые могут быть в ответе
    if parse_mode == 'MarkdownV2':
        # Базовое экранирование для самых частых проблемных символов
        escape_chars = '_*[]()~`>#+-=|{}.!'
        for char in escape_chars:
            response_text = response_text.replace(char, f'\\{char}')
        
    bot.send_message(message.chat.id, response_text, parse_mode=parse_mode)


# --- Запуск бота ---
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)