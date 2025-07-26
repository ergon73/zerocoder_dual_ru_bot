#!/bin/bash

# Скрипт для настройки SSH доступа к VPS
# IP: 158.160.53.164
# Пользователь: ergon73

VPS_IP="158.160.53.164"
VPS_USER="ergon73"

echo "🔑 Настройка SSH доступа к VPS ${VPS_IP}..."

# Проверяем наличие SSH ключей
if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "❌ SSH ключ не найден. Создайте ключ: ssh-keygen -t ed25519"
    exit 1
fi

# Читаем публичный ключ
PUBLIC_KEY=$(cat ~/.ssh/id_ed25519.pub)

echo "📋 Ваш публичный ключ:"
echo "${PUBLIC_KEY}"
echo ""

echo "📝 Инструкция по настройке SSH доступа:"
echo ""
echo "1. Подключитесь к VPS через веб-консоль или панель управления"
echo "2. Выполните следующие команды на VPS:"
echo ""
echo "   # Создаем .ssh директорию (если не существует)"
echo "   mkdir -p ~/.ssh"
echo ""
echo "   # Добавляем ваш публичный ключ"
echo "   echo '${PUBLIC_KEY}' >> ~/.ssh/authorized_keys"
echo ""
echo "   # Устанавливаем правильные права"
echo "   chmod 700 ~/.ssh"
echo "   chmod 600 ~/.ssh/authorized_keys"
echo ""
echo "3. Проверьте подключение:"
echo "   ssh ${VPS_USER}@${VPS_IP}"
echo ""
echo "4. После успешного подключения можно использовать автоматическое развертывание:"
echo "   ./deploy_to_vps.sh"
echo ""

# Альтернативный способ через ssh-copy-id
echo "🔄 Альтернативный способ (если у вас есть пароль от VPS):"
echo "   ssh-copy-id ${VPS_USER}@${VPS_IP}"
echo ""

echo "✅ Инструкция готова!" 