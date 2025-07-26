# PowerShell скрипт для настройки SSH доступа к VPS
# IP: your_vps_ip
# Пользователь: your_vps_user

$VPS_IP = "your_vps_ip"
$VPS_USER = "your_vps_user"

Write-Host "🔑 Настройка SSH доступа к VPS" -ForegroundColor Green
Write-Host ""

# Проверяем наличие публичного ключа
if (Test-Path "$env:USERPROFILE\.ssh\id_ed25519.pub") {
    Write-Host "📋 Ваш публичный ключ (id_ed25519.pub):" -ForegroundColor Yellow
    Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub"
    Write-Host ""
    Write-Host "📝 Инструкции для настройки на VPS:" -ForegroundColor Yellow
    Write-Host "1. Подключитесь к VPS через веб-консоль"
    Write-Host "2. Выполните команды:"
    Write-Host "   mkdir -p ~/.ssh"
    Write-Host "   echo `"$(Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub")`" >> ~/.ssh/authorized_keys"
    Write-Host "   chmod 700 ~/.ssh"
    Write-Host "   chmod 600 ~/.ssh/authorized_keys"
    Write-Host ""
    Write-Host "3. Проверьте подключение:"
    Write-Host "   ssh ${VPS_USER}@${VPS_IP}"
    Write-Host ""
    Write-Host "💡 Альтернативно, если у вас есть пароль от VPS:"
    Write-Host "   ssh-copy-id ${VPS_USER}@${VPS_IP}"
} else {
    Write-Host "❌ Публичный ключ ~/.ssh/id_ed25519.pub не найден" -ForegroundColor Red
    Write-Host "Создайте SSH ключ командой: ssh-keygen -t ed25519" -ForegroundColor Yellow
} 