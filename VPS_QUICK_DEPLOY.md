# Быстрое развертывание на VPS

**VPS IP:** 158.160.53.164  
**Пользователь:** ergon73

## Шаг 1: Подключение к VPS

```bash
ssh ergon73@158.160.53.164
```

## Шаг 2: Проверка Docker

```bash
# Проверяем Docker
docker --version

# Проверяем Docker Compose
docker-compose --version

# Если Docker Compose не установлен:
sudo apt update
sudo apt install docker-compose
```

## Шаг 3: Создание проекта

```bash
# Создаем папку проекта
mkdir dual-ru-bot
cd dual-ru-bot
```

## Шаг 4: Создание .env файла

```bash
nano .env
```

Содержимое `.env`:
```env
# Telegram Bot Token
TELEGRAM_BOT_TOKEN=ваш_токен_бота

# GigaChat credentials
GIGACHAT_CREDENTIALS=ваши_gigachat_credentials
GIGACHAT_CERT_PATH=russian_trusted_root_ca.cer

# YandexGPT credentials
YANDEX_FOLDER_ID=ваш_yandex_folder_id
YANDEX_API_KEY=ваш_yandex_api_key
```

## Шаг 5: Добавление сертификата

```bash
# Скопируйте файл russian_trusted_root_ca.cer в папку dual-ru-bot
# Используйте scp или любой другой способ
```

## Шаг 6: Создание docker-compose.prod.yml

```bash
nano docker-compose.prod.yml
```

Содержимое:
```yaml
version: '3.8'

services:
  telegram-bot:
    image: ergon73/dual-ru-bot:latest
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

## Шаг 7: Запуск бота

```bash
# Скачиваем образ из Docker Hub
docker pull ergon73/dual-ru-bot:latest

# Создаем директорию для логов
mkdir -p logs

# Запускаем контейнер
docker-compose -f docker-compose.prod.yml up -d

# Проверяем статус
docker-compose -f docker-compose.prod.yml ps
```

## Шаг 8: Проверка работы

```bash
# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f

# Проверка контейнера
docker ps

# Проверка переменных окружения
docker exec dual-ru-bot env | grep -E "(TELEGRAM|GIGACHAT|YANDEX)"
```

## Управление ботом

### Просмотр логов
```bash
# Логи в реальном времени
docker-compose -f docker-compose.prod.yml logs -f

# Последние 100 строк
docker-compose -f docker-compose.prod.yml logs --tail=100
```

### Остановка/Запуск
```bash
# Остановка
docker-compose -f docker-compose.prod.yml down

# Запуск
docker-compose -f docker-compose.prod.yml up -d

# Перезапуск
docker-compose -f docker-compose.prod.yml restart
```

### Обновление
```bash
# Остановка
docker-compose -f docker-compose.prod.yml down

# Скачивание нового образа
docker pull ergon73/dual-ru-bot:latest

# Запуск
docker-compose -f docker-compose.prod.yml up -d
```

## Устранение неполадок

### Проверка статуса
```bash
# Статус контейнера
docker-compose -f docker-compose.prod.yml ps

# Детальная информация
docker inspect dual-ru-bot

# Логи с ошибками
docker-compose -f docker-compose.prod.yml logs | grep ERROR
```

### Проверка файлов
```bash
# Проверка .env
cat .env

# Проверка сертификата
ls -la russian_trusted_root_ca.cer

# Проверка docker-compose файла
cat docker-compose.prod.yml
```

### Перезапуск при проблемах
```bash
# Полный перезапуск
docker-compose -f docker-compose.prod.yml down
docker system prune -f
docker-compose -f docker-compose.prod.yml up -d
```

## Мониторинг

### Использование ресурсов
```bash
# Мониторинг CPU и памяти
docker stats dual-ru-bot
```

### Логирование
Логи доступны в папке `logs/` и через Docker:
```bash
# Логи приложения
tail -f logs/bot.log

# Логи контейнера
docker-compose -f docker-compose.prod.yml logs -f
```

## Готово! 🎉

После выполнения всех шагов ваш Telegram бот будет работать на VPS 158.160.53.164.

**Проверьте бота в Telegram:** отправьте `/start` вашему боту. 