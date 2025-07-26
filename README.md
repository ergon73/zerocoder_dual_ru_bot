# Dual Russian LLM Bot

Telegram бот с поддержкой двух русскоязычных LLM моделей: GigaChat и YandexGPT.

## Возможности

- Переключение между моделями через команды `/giga` и `/yandex`
- Поддержка GigaChat от Сбера
- Поддержка YandexGPT от Яндекса
- Удобное меню для выбора модели
- Подробное логирование для диагностики
- Docker контейнеризация для развертывания на VPS
- Готовый образ в Docker Hub

## Установка

### Локальная установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your_github_username/zerocoder_dual_ru_bot.git
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

### Docker развертывание (локальное)

1. Убедитесь, что у вас установлены Docker и Docker Compose:
```bash
docker --version
docker-compose --version
```

2. Клонируйте репозиторий и перейдите в папку проекта:
```bash
git clone https://github.com/your_github_username/zerocoder_dual_ru_bot.git
cd zerocoder_dual_ru_bot
```

3. Создайте файл `.env` с переменными окружения (см. выше)

4. Поместите сертификат `russian_trusted_root_ca.cer` в корневую папку проекта

5. Запустите развертывание:
```bash
# Автоматическое развертывание
chmod +x deploy.sh
./deploy.sh

# Или вручную
docker-compose up -d --build
```

6. Проверьте статус контейнера:
```bash
docker-compose ps
docker-compose logs -f
```

### Docker Hub развертывание (рекомендуется для VPS)

#### Публикация образа в Docker Hub

1. Авторизуйтесь в Docker Hub:
```bash
docker login
```

2. Опубликуйте образ:
```bash
chmod +x publish_to_dockerhub.sh
./publish_to_dockerhub.sh
```

#### Развертывание на VPS

1. Подключитесь к VPS по SSH

2. Установите Docker и Docker Compose:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
```

3. Создайте папку для проекта:
```bash
mkdir dual-ru-bot
cd dual-ru-bot
```

4. Создайте файл `.env` с переменными окружения

5. Скачайте сертификат:
```bash
# Скопируйте russian_trusted_root_ca.cer в папку проекта
```

6. Создайте `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  telegram-bot:
    image: your_docker_username/dual-ru-bot:latest
    container_name: dual-ru-bot
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - GIGACHAT_CREDENTIALS=${GIGACHAT_CREDENTIALS}
      - GIGACHAT_CERT_PATH=${GIGACHAT_CERT_PATH}
      - YANDEX_FOLDER_ID=${YANDEX_FOLDER_ID}
      - YANDEX_API_KEY=${YANDEX_API_KEY}
    volumes:
      - ./logs:/app/logs
      - ./russian_trusted_root_ca.cer:/app/russian_trusted_root_ca.cer:ro
    networks:
      - bot-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  bot-network:
    driver: bridge
```

7. Запустите бота:
```bash
docker-compose -f docker-compose.prod.yml up -d
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

### Локальный запуск
```bash
python dual_ru_bot.py
```

### Docker запуск (локальный)
```bash
# Запуск в фоновом режиме
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### Docker Hub запуск (VPS)
```bash
# Запуск в фоновом режиме
docker-compose -f docker-compose.prod.yml up -d

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f

# Остановка
docker-compose -f docker-compose.prod.yml down
```

## Использование

1. Запустите бота командой `/start`
2. Выберите модель через меню или используйте команды:
   - `/giga` - переключиться на GigaChat
   - `/yandex` - переключиться на YandexGPT
3. Отправляйте сообщения боту и получайте ответы от выбранной модели

## Требования

- Python 3.7+ (для локального запуска)
- Docker и Docker Compose (для контейнеризации)
- Токен Telegram бота
- Доступ к API GigaChat
- Доступ к API YandexGPT
- Сертификат SSL для GigaChat

## Логирование

Бот ведет подробный лог в файл `bot.log` (локально) или в контейнере. Логи включают:
- Все входящие и исходящие сообщения
- Информацию о пользователях (ID, username, имя)
- Детали запросов к LLM API
- Ошибки и исключения

### Просмотр логов в Docker
```bash
# Логи в реальном времени
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs telegram-bot

# Последние 100 строк
docker-compose logs --tail=100 telegram-bot
```

### Просмотр логов в Docker Hub версии
```bash
# Логи в реальном времени
docker-compose -f docker-compose.prod.yml logs -f

# Логи конкретного сервиса
docker-compose -f docker-compose.prod.yml logs telegram-bot

# Последние 100 строк
docker-compose -f docker-compose.prod.yml logs --tail=100 telegram-bot
```

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

## Развертывание на VPS

### Быстрое развертывание через Docker Hub

1. Подключитесь к вашему VPS по SSH
2. Установите Docker и Docker Compose
3. Создайте папку для проекта и перейдите в неё
4. Создайте файл `.env` с переменными окружения
5. Поместите сертификат `russian_trusted_root_ca.cer` в папку проекта
6. Создайте `docker-compose.prod.yml` (см. выше)
7. Запустите `docker-compose -f docker-compose.prod.yml up -d`

### Интеграция с Better Stack

Если у вас настроена интеграция Docker с Better Stack для логирования:
1. Убедитесь, что Docker контейнер отправляет логи в Better Stack
2. Логи бота будут автоматически доступны в панели Better Stack
3. Настройте алерты для критических ошибок

## Docker Hub

Образ доступен в Docker Hub: `your_docker_username/dual-ru-bot:latest`

### Использование образа

```bash
# Скачать образ
docker pull your_docker_username/dual-ru-bot:latest

# Запустить контейнер
docker run -d \
  --name dual-ru-bot \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/russian_trusted_root_ca.cer:/app/russian_trusted_root_ca.cer:ro \
  your_docker_username/dual-ru-bot:latest
```

## Контакты

По вопросам работы бота обращайтесь: your_email@example.com

## Лицензия

MIT License 