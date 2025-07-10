import os
import logging
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

# Настройка логирования
logger = logging.getLogger(__name__)

# Этот модуль будет отвечать за всю логику работы с GigaChat.
# Мы используем библиотеку gigachat, как и предлагалось в уроке.

# Проверяем наличие необходимых переменных окружения
credentials = os.getenv("GIGACHAT_CREDENTIALS")
cert_path = os.getenv("GIGACHAT_CERT_PATH", "russian_trusted_root_ca.cer")

if not credentials:
    logger.error("Не найдены учетные данные GigaChat в переменных окружения")
    raise ValueError("GIGACHAT_CREDENTIALS не найден в переменных окружения")

if not os.path.exists(cert_path):
    logger.warning(f"Файл сертификата {cert_path} не найден")

# Заранее создаем объект GigaChat
try:
    logger.debug("Инициализация клиента GigaChat")
    giga: GigaChat = GigaChat(
        credentials=credentials,
        ca_bundle_file=cert_path,
        verify_ssl_certs=True
    )
    logger.info("Клиент GigaChat успешно инициализирован")
except Exception as e:
    logger.error(f"Ошибка при инициализации GigaChat: {str(e)}")
    raise

def get_giga_response(user_prompt: str) -> str:
    """
    Отправляет запрос к GigaChat и возвращает ответ.
    В случае ошибки возвращает сообщение об ошибке.
    """
    try:
        credentials = os.getenv("GIGACHAT_CREDENTIALS")
        cert_path = os.getenv("GIGACHAT_CERT_PATH", "russian_trusted_root_ca.cer")

        if not credentials:
            logger.error("Не найдены учетные данные GigaChat в переменных окружения")
            return "Не удалось получить ответ от GigaChat: отсутствуют учетные данные"

        # Проверяем наличие сертификата
        if not os.path.exists(cert_path):
            logger.warning(f"Сертификат {cert_path} не найден")
            cert_path = None
        
        # Создаем клиент GigaChat
        giga = GigaChat(
            credentials=credentials,
            verify_ssl_certs=False,  # Отключаем проверку SSL для тестов
            ca_bundle=cert_path
        )
        
        # Создаем структуру сообщения для API
        messages = [
            Messages(
                role=MessagesRole.SYSTEM,
                content="Ты — полезный ассистент."
            ),
            Messages(
                role=MessagesRole.USER,
                content=user_prompt
            )
        ]
        
        # Отправляем запрос
        response = giga.chat(Chat(messages=messages))
        
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Ошибка при работе с GigaChat: {str(e)}")
        return "Не удалось получить ответ от GigaChat. Попробуйте позже."