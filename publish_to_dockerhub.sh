#!/bin/bash

# Скрипт для публикации Telegram бота в Docker Hub
# Использование: ./publish_to_dockerhub.sh

set -e

# Конфигурация
DOCKER_USERNAME="ergon73"
IMAGE_NAME="dual-ru-bot"
VERSION="1.0.0"
FULL_IMAGE_NAME="${DOCKER_USERNAME}/${IMAGE_NAME}"

echo "🐳 Начинаем публикацию в Docker Hub..."

# Проверяем, что мы в правильной директории
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile не найден. Убедитесь, что вы в корневой папке проекта."
    exit 1
fi

# Проверяем наличие .env файла (для локального тестирования)
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден. Создайте его для локального тестирования."
fi

# Проверяем наличие сертификата
if [ ! -f "russian_trusted_root_ca.cer" ]; then
    echo "❌ Файл russian_trusted_root_ca.cer не найден. Поместите его в корневую папку проекта."
    exit 1
fi

echo "✅ Все проверки пройдены"

# Собираем образ с тегом версии
echo "🔨 Собираем образ ${FULL_IMAGE_NAME}:${VERSION}..."
docker build -t "${FULL_IMAGE_NAME}:${VERSION}" .
docker tag "${FULL_IMAGE_NAME}:${VERSION}" "${FULL_IMAGE_NAME}:latest"

# Собираем образ с тегом latest
echo "🔨 Собираем образ ${FULL_IMAGE_NAME}:latest..."
docker build -t "${FULL_IMAGE_NAME}:latest" .

echo "📦 Образы собраны успешно!"

# Проверяем, авторизован ли пользователь в Docker Hub
if ! docker info | grep -q "Username"; then
    echo "🔐 Требуется авторизация в Docker Hub"
    echo "Выполните: docker login"
    echo "Или используйте токен: docker login -u ${DOCKER_USERNAME}"
    exit 1
fi

# Публикуем образы
echo "🚀 Публикуем образы в Docker Hub..."

echo "📤 Публикуем ${FULL_IMAGE_NAME}:${VERSION}..."
docker push "${FULL_IMAGE_NAME}:${VERSION}"

echo "📤 Публикуем ${FULL_IMAGE_NAME}:latest..."
docker push "${FULL_IMAGE_NAME}:latest"

echo "✅ Публикация завершена!"
echo ""
echo "📋 Информация об образах:"
echo "   - ${FULL_IMAGE_NAME}:${VERSION}"
echo "   - ${FULL_IMAGE_NAME}:latest"
echo ""
echo "🔗 Ссылка на Docker Hub:"
echo "   https://hub.docker.com/r/${DOCKER_USERNAME}/${IMAGE_NAME}"
echo ""
echo "📝 Для использования на VPS:"
echo "   docker pull ${FULL_IMAGE_NAME}:latest"
echo ""
echo "🎉 Образы успешно опубликованы в Docker Hub!" 