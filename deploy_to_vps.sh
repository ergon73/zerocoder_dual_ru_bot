#!/bin/bash

# Скрипт для развертывания Telegram бота на VPS
# IP: your_vps_ip
# Использование: ./deploy_to_vps.sh

set -e

VPS_IP="your_vps_ip"
VPS_USER="your_vps_user"
PROJECT_NAME="dual-ru-bot"

echo "🚀 Начинаем развертывание на VPS ${VPS_IP}..."

# Проверяем наличие SSH ключей
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "❌ SSH ключ не найден. Убедитесь, что у вас настроен SSH доступ к VPS."
    exit 1
fi

# Проверяем подключение к VPS
echo "🔍 Проверяем подключение к VPS..."
if ! ssh -o ConnectTimeout=10 -o BatchMode=yes ${VPS_USER}@${VPS_IP} "echo 'SSH подключение работает'" 2>/dev/null; then
    echo "❌ Не удается подключиться к VPS. Проверьте SSH настройки."
    exit 1
fi

echo "✅ Подключение к VPS успешно"

# Создаем docker-compose.prod.yml для VPS
echo "📝 Создаем docker-compose.prod.yml..."
cat > docker-compose.prod.yml << 'EOF'
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
EOF

# Создаем скрипт развертывания для VPS
echo "📝 Создаем скрипт развертывания для VPS..."
cat > vps_deploy.sh << 'EOF'
#!/bin/bash

set -e

echo "🚀 Развертывание Telegram бота на VPS..."

# Проверяем Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен"
    exit 1
fi

# Проверяем Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Устанавливаем Docker Compose..."
    sudo apt update
    sudo apt install -y docker-compose
fi

# Создаем папку проекта
mkdir -p ${PROJECT_NAME}
cd ${PROJECT_NAME}

# Останавливаем существующий контейнер
docker-compose -f docker-compose.prod.yml down || true

# Удаляем старый образ
docker rmi your_docker_username/dual-ru-bot:latest || true

# Создаем директорию для логов
mkdir -p logs

# Скачиваем последний образ
echo "📥 Скачиваем образ из Docker Hub..."
docker pull your_docker_username/dual-ru-bot:latest

# Запускаем контейнер
echo "🚀 Запускаем контейнер..."
docker-compose -f docker-compose.prod.yml up -d

# Проверяем статус
echo "📊 Статус контейнера:"
docker-compose -f docker-compose.prod.yml ps

echo "✅ Развертывание завершено!"
echo "📝 Логи: docker-compose -f docker-compose.prod.yml logs -f"
EOF

chmod +x vps_deploy.sh

# Копируем файлы на VPS
echo "📤 Копируем файлы на VPS..."
scp docker-compose.prod.yml ${VPS_USER}@${VPS_IP}:~/
scp vps_deploy.sh ${VPS_USER}@${VPS_IP}:~/

# Создаем .env файл на VPS (если его нет)
echo "📝 Создаем .env файл на VPS..."
ssh ${VPS_USER}@${VPS_IP} "if [ ! -f .env ]; then echo 'Создайте файл .env с переменными окружения'; fi"

# Запускаем развертывание на VPS
echo "🚀 Запускаем развертывание на VPS..."
ssh ${VPS_USER}@${VPS_IP} "chmod +x vps_deploy.sh && ./vps_deploy.sh"

echo "✅ Развертывание завершено!"
echo ""
echo "📋 Полезные команды для управления ботом:"
echo "   SSH: ssh ${VPS_USER}@${VPS_IP}"
echo "   Логи: docker-compose -f docker-compose.prod.yml logs -f"
echo "   Статус: docker-compose -f docker-compose.prod.yml ps"
echo "   Остановка: docker-compose -f docker-compose.prod.yml down"
echo "   Перезапуск: docker-compose -f docker-compose.prod.yml restart"
echo ""
echo "🎉 Бот развернут на VPS ${VPS_IP}!" 