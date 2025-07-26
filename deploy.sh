#!/bin/bash

# Скрипт для развертывания Telegram бота на VPS
# Использование: ./deploy.sh

set -e

echo "🚀 Начинаем развертывание Telegram бота..."

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker сначала."
    exit 1
fi

# Проверяем наличие docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose сначала."
    exit 1
fi

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден. Создайте его с переменными окружения."
    exit 1
fi

# Проверяем наличие сертификата
if [ ! -f russian_trusted_root_ca.cer ]; then
    echo "❌ Файл russian_trusted_root_ca.cer не найден. Поместите его в корневую папку проекта."
    exit 1
fi

echo "✅ Все проверки пройдены"

# Останавливаем существующий контейнер
echo "🛑 Останавливаем существующий контейнер..."
docker-compose down || true

# Удаляем старый образ
echo "🗑️ Удаляем старый образ..."
docker rmi dual-ru-bot:latest || true

# Создаем директорию для логов
echo "📁 Создаем директорию для логов..."
mkdir -p logs

# Собираем новый образ
echo "🔨 Собираем новый образ..."
docker-compose build --no-cache

# Запускаем контейнер
echo "🚀 Запускаем контейнер..."
docker-compose up -d

# Проверяем статус
echo "📊 Проверяем статус контейнера..."
docker-compose ps

echo "✅ Развертывание завершено!"
echo "📝 Логи доступны в папке logs/"
echo "🔍 Для просмотра логов используйте: docker-compose logs -f" 