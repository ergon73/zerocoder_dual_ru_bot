# Dual Russian LLM Bot

Telegram бот с поддержкой двух русскоязычных LLM моделей: GigaChat и YandexGPT.

## Возможности

- Переключение между моделями через команды `/giga` и `/yandex`
- Поддержка GigaChat от Сбера
- Поддержка YandexGPT от Яндекса
- Удобное меню для выбора модели
- Подробное логирование для диагностики

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ergon73/zerocoder_dual_ru_bot.git
cd zerocoder_dual_ru_bot
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
# или
.venv\Scripts\activate  # для Windows
pip install -r requirements.txt
```

3. Создайте файл `.env` в корневой директории проекта со следующими переменными:
```
# Telegram Bot Token (получить у @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# GigaChat credentials (получить в личном кабинете https://developers.sber.ru/portal/products/gigachat)
GIGACHAT_CREDENTIALS=your_gigachat_credentials
GIGACHAT_CERT_PATH=russian_trusted_root_ca.cer  # Путь к сертификату (по умолчанию в корневой папке)

# YandexGPT credentials (получить в консоли Yandex Cloud)
YANDEX_FOLDER_ID=your_yandex_folder_id
YANDEX_API_KEY=your_yandex_api_key
```

## Получение доступа к API

### Telegram Bot
1. Создайте нового бота у [@BotFather](https://t.me/BotFather)
2. Получите токен бота и добавьте его в `.env`

### GigaChat
1. Зарегистрируйтесь на [портале разработчиков Сбера](https://developers.sber.ru/portal/products/gigachat)
2. Получите credentials для доступа к API
3. Скачайте сертификат `russian_trusted_root_ca.cer` и поместите его в корневую папку проекта
   - Сертификат необходим для SSL-подключения к API GigaChat
   - По умолчанию код ищет файл `russian_trusted_root_ca.cer` в корневой папке
   - Вы можете указать другой путь через переменную `GIGACHAT_CERT_PATH` в `.env`

### YandexGPT
1. Создайте проект в [консоли Yandex Cloud](https://console.cloud.yandex.ru/)
2. Создайте сервисный аккаунт и получите API-ключ
3. Скопируйте ID каталога (folder_id)

## Запуск

```bash
python dual_ru_bot.py
```

## Использование

1. Запустите бота командой `/start`
2. Выберите модель через меню или используйте команды:
   - `/giga` - переключиться на GigaChat
   - `/yandex` - переключиться на YandexGPT
3. Отправляйте сообщения боту и получайте ответы от выбранной модели

## Требования

- Python 3.7+
- Токен Telegram бота
- Доступ к API GigaChat
- Доступ к API YandexGPT
- Сертификат SSL для GigaChat

## Логирование

Бот ведет подробный лог в файл `bot.log`. Это помогает в отладке и диагностике проблем.

## Тестирование

Проект использует pytest для модульного тестирования. Тесты находятся в директории `tests/`.

Для запуска тестов:
```bash
# Установка зависимостей для тестирования
pip install -r requirements.txt

# Запуск всех тестов
pytest

# Запуск тестов с подробным выводом
pytest -v

# Запуск конкретного теста
pytest tests/test_yandex_helper.py
```

## Контакты

По вопросам работы бота обращайтесь: georgy.belyanin@gmail.com

## Лицензия

MIT License 