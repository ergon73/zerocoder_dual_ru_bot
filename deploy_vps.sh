#!/bin/bash

# Упрощенный скрипт развертывания Telegram бота на VPS
# Использует образ из Docker Hub
# Использование: ./deploy_vps.sh

set -e

echo "🚀 Начинаем развертывание Telegram бота на VPS..."

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
docker-compose -f docker-compose.prod.yml down || true

# Удаляем старый образ (если есть)
echo "🗑️ Удаляем старый образ..."
docker rmi ergon73/dual-ru-bot:latest || true

# Создаем директорию для логов
echo "📁 Создаем директорию для логов..."
mkdir -p logs

# Скачиваем последний образ из Docker Hub
echo "📥 Скачиваем образ из Docker Hub..."
docker pull ergon73/dual-ru-bot:latest

# Запускаем контейнер
echo "🚀 Запускаем контейнер..."
docker-compose -f docker-compose.prod.yml up -d

# Проверяем статус
echo "📊 Проверяем статус контейнера..."
docker-compose -f docker-compose.prod.yml ps

echo "✅ Развертывание завершено!"
echo "📝 Логи доступны в папке logs/"
echo "🔍 Для просмотра логов используйте: docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "🎉 Бот успешно развернут на VPS!" 