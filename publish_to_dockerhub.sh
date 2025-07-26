#!/bin/bash

# Скрипт для публикации Docker образа в Docker Hub
# Использование: ./publish_to_dockerhub.sh

set -e

DOCKER_USERNAME="your_docker_username"
IMAGE_NAME="dual-ru-bot"
VERSION="1.0.0"

echo "🚀 Публикация Docker образа в Docker Hub..."

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен"
    exit 1
fi

# Собираем образ с версией
echo "🔨 Собираем образ ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}..."
docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION} .

# Собираем образ с тегом latest
echo "🔨 Собираем образ ${DOCKER_USERNAME}/${IMAGE_NAME}:latest..."
docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME}:latest .

# Проверяем авторизацию в Docker Hub
if ! docker info | grep -q "Username"; then
    echo "🔐 Требуется авторизация в Docker Hub"
    echo "Выполните: docker login"
    docker login
fi

# Публикуем образы
echo "📤 Публикуем образ ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}..."
docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}

echo "📤 Публикуем образ ${DOCKER_USERNAME}/${IMAGE_NAME}:latest..."
docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:latest

echo "✅ Публикация завершена!"
echo "📋 Образы доступны в Docker Hub:"
echo "   - ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"
echo "   - ${DOCKER_USERNAME}/${IMAGE_NAME}:latest" 