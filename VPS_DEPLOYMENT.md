# Развертывание Telegram бота на VPS

Подробная инструкция по развертыванию Dual Russian LLM Bot на VPS с интеграцией Better Stack для логирования.

## Подготовка VPS

### 1. Установка Docker и Docker Compose

```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Устанавливаем Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезагружаемся для применения изменений
sudo reboot
```

### 2. Настройка Better Stack

1. Создайте аккаунт на [Better Stack](https://betterstack.com/)
2. Создайте новый источник логов (Log Source)
3. Получите токен для отправки логов
4. Настройте Docker logging driver

```bash
# Создаем файл конфигурации Docker daemon
sudo nano /etc/docker/daemon.json
```

Добавьте следующую конфигурацию:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Перезапустите Docker:
```bash
sudo systemctl restart docker
```

## Развертывание бота

### 1. Клонирование репозитория

```bash
# Клонируем репозиторий
git clone https://github.com/your_github_username/zerocoder_dual_ru_bot.git
cd zerocoder_dual_ru_bot
```

### 2. Настройка переменных окружения

Создайте файл `.env`:
```bash
nano .env
```

Добавьте ваши переменные окружения:
```env
# Telegram Bot Token
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# GigaChat credentials
GIGACHAT_CREDENTIALS=your_gigachat_credentials
GIGACHAT_CERT_PATH=russian_trusted_root_ca.cer

# YandexGPT credentials
YANDEX_FOLDER_ID=your_yandex_folder_id
YANDEX_API_KEY=your_yandex_api_key
```

### 3. Добавление сертификата

Поместите файл `russian_trusted_root_ca.cer` в корневую папку проекта:
```bash
# Скопируйте сертификат в папку проекта
cp /path/to/russian_trusted_root_ca.cer .
```

### 4. Запуск развертывания

```bash
# Делаем скрипт исполняемым
chmod +x deploy.sh

# Запускаем развертывание
./deploy.sh
```

Или вручную:
```bash
# Собираем образ
docker-compose build --no-cache

# Запускаем контейнер
docker-compose up -d

# Проверяем статус
docker-compose ps
```

## Мониторинг и логирование

### 1. Просмотр логов в реальном времени

```bash
# Логи контейнера
docker-compose logs -f telegram-bot

# Логи с последними 100 строками
docker-compose logs --tail=100 telegram-bot

# Логи с временными метками
docker-compose logs -f --timestamps telegram-bot
```

### 2. Интеграция с Better Stack

Для отправки логов в Better Stack, обновите `docker-compose.yml`:

```yaml
version: '3.8'

services:
  telegram-bot:
    build: .
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

### 3. Настройка алертов в Better Stack

1. Создайте алерт для ошибок:
   - Условие: `level = "ERROR"`
   - Уведомления: email, Slack, или другие каналы

2. Создайте алерт для высокой нагрузки:
   - Условие: количество сообщений > 100 в минуту
   - Уведомления: для мониторинга производительности

## Управление контейнером

### Основные команды

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Обновление (после изменений в коде)
docker-compose up -d --build

# Просмотр ресурсов
docker stats dual-ru-bot

# Вход в контейнер для отладки
docker exec -it dual-ru-bot /bin/bash
```

### Обновление бота

```bash
# Останавливаем контейнер
docker-compose down

# Получаем обновления из Git
git pull origin main

# Пересобираем и запускаем
docker-compose up -d --build
```

## Безопасность

### 1. Настройка файрвола

```bash
# Устанавливаем UFW
sudo apt install ufw

# Настраиваем правила
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Включаем файрвол
sudo ufw enable
```

### 2. Регулярные обновления

```bash
# Создаем скрипт для автоматических обновлений
nano update-bot.sh
```

Содержимое скрипта:
```bash
#!/bin/bash
cd /path/to/zerocoder_dual_ru_bot
git pull origin main
docker-compose down
docker-compose up -d --build
```

```bash
# Делаем исполняемым
chmod +x update-bot.sh

# Добавляем в cron для автоматических обновлений
crontab -e
# Добавьте строку для ежедневного обновления в 3:00
0 3 * * * /path/to/update-bot.sh
```

## Устранение неполадок

### 1. Проверка статуса контейнера

```bash
# Статус контейнера
docker-compose ps

# Детальная информация
docker inspect dual-ru-bot

# Логи с ошибками
docker-compose logs --tail=50 telegram-bot | grep ERROR
```

### 2. Проверка переменных окружения

```bash
# Проверка переменных в контейнере
docker exec dual-ru-bot env | grep -E "(TELEGRAM|GIGACHAT|YANDEX)"
```

### 3. Проверка сертификата

```bash
# Проверка наличия сертификата в контейнере
docker exec dual-ru-bot ls -la /app/russian_trusted_root_ca.cer
```

### 4. Перезапуск при проблемах

```bash
# Полный перезапуск
docker-compose down
docker system prune -f
docker-compose up -d --build
```

## Мониторинг производительности

### 1. Использование ресурсов

```bash
# Мониторинг CPU и памяти
docker stats dual-ru-bot

# Детальная информация о ресурсах
docker exec dual-ru-bot cat /proc/meminfo
docker exec dual-ru-bot cat /proc/cpuinfo
```

### 2. Логирование производительности

Логи в JSON формате уже включают метрики:
- Время обработки запросов
- Длина сообщений
- Используемая модель
- Количество пользователей

### 3. Алерты в Better Stack

Настройте алерты для:
- Высокого потребления CPU (>80%)
- Высокого потребления памяти (>80%)
- Большого количества ошибок
- Медленной обработки запросов

## Резервное копирование

### 1. Резервное копирование логов

```bash
# Создаем скрипт для бэкапа
nano backup-logs.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "bot-logs-$DATE.tar.gz" logs/
# Отправляем в облачное хранилище или другой сервер
```

### 2. Резервное копирование конфигурации

```bash
# Бэкап .env файла
cp .env .env.backup

# Бэкап docker-compose.yml
cp docker-compose.yml docker-compose.yml.backup
```

## Заключение

После выполнения всех шагов ваш Telegram бот будет:
- Работать в Docker контейнере на VPS
- Автоматически перезапускаться при сбоях
- Отправлять структурированные логи в Better Stack
- Мониториться через алерты и дашборды
- Безопасно обновляться

Для получения помощи обращайтесь: your_email@example.com 