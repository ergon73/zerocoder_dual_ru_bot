#!/bin/bash

# IP: your_vps_ip
# Пользователь: your_vps_user

VPS_IP="your_vps_ip"
VPS_USER="your_vps_user"

echo "🔑 Настройка SSH доступа к VPS"
echo ""

# Проверяем наличие публичного ключа
if [ -f ~/.ssh/id_ed25519.pub ]; then
    echo "📋 Ваш публичный ключ (id_ed25519.pub):"
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "📝 Инструкции для настройки на VPS:"
    echo "1. Подключитесь к VPS через веб-консоль"
    echo "2. Выполните команды:"
    echo "   mkdir -p ~/.ssh"
    echo "   echo \"$(cat ~/.ssh/id_ed25519.pub)\" >> ~/.ssh/authorized_keys"
    echo "   chmod 700 ~/.ssh"
    echo "   chmod 600 ~/.ssh/authorized_keys"
    echo ""
    echo "3. Проверьте подключение:"
    echo "   ssh ${VPS_USER}@${VPS_IP}"
    echo ""
    echo "💡 Альтернативно, если у вас есть пароль от VPS:"
    echo "   ssh-copy-id ${VPS_USER}@${VPS_IP}"
else
    echo "❌ Публичный ключ ~/.ssh/id_ed25519.pub не найден"
    echo "Создайте SSH ключ командой: ssh-keygen -t ed25519"
fi 