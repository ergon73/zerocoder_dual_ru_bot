# PowerShell скрипт для настройки SSH доступа к VPS
# IP: 158.160.53.164
# Пользователь: ergon73

$VPS_IP = "158.160.53.164"
$VPS_USER = "ergon73"

Write-Host "🔑 Настройка SSH доступа к VPS ${VPS_IP}..." -ForegroundColor Green

# Проверяем наличие SSH ключей
$sshPath = "$env:USERPROFILE\.ssh"
$keyPath = "$sshPath\id_ed25519"
$pubKeyPath = "$sshPath\id_ed25519.pub"

if (-not (Test-Path $keyPath)) {
    Write-Host "❌ SSH ключ не найден в $keyPath" -ForegroundColor Red
    Write-Host "Создайте ключ: ssh-keygen -t ed25519" -ForegroundColor Yellow
    exit 1
}

# Читаем публичный ключ
$PUBLIC_KEY = Get-Content $pubKeyPath -Raw

Write-Host "📋 Ваш публичный ключ:" -ForegroundColor Cyan
Write-Host $PUBLIC_KEY -ForegroundColor White
Write-Host ""

Write-Host "📝 Инструкция по настройке SSH доступа:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Подключитесь к VPS через веб-консоль или панель управления" -ForegroundColor White
Write-Host "2. Выполните следующие команды на VPS:" -ForegroundColor White
Write-Host ""
Write-Host "   # Создаем .ssh директорию (если не существует)" -ForegroundColor Gray
Write-Host "   mkdir -p ~/.ssh" -ForegroundColor Gray
Write-Host ""
Write-Host "   # Добавляем ваш публичный ключ" -ForegroundColor Gray
Write-Host "   echo '$PUBLIC_KEY' >> ~/.ssh/authorized_keys" -ForegroundColor Gray
Write-Host ""
Write-Host "   # Устанавливаем правильные права" -ForegroundColor Gray
Write-Host "   chmod 700 ~/.ssh" -ForegroundColor Gray
Write-Host "   chmod 600 ~/.ssh/authorized_keys" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Проверьте подключение:" -ForegroundColor White
Write-Host "   ssh ${VPS_USER}@${VPS_IP}" -ForegroundColor Gray
Write-Host ""
Write-Host "4. После успешного подключения можно использовать автоматическое развертывание:" -ForegroundColor White
Write-Host "   ./deploy_to_vps.sh" -ForegroundColor Gray
Write-Host ""

# Альтернативный способ через ssh-copy-id
Write-Host "🔄 Альтернативный способ (если у вас есть пароль от VPS):" -ForegroundColor Yellow
Write-Host "   ssh-copy-id ${VPS_USER}@${VPS_IP}" -ForegroundColor Gray
Write-Host ""

Write-Host "✅ Инструкция готова!" -ForegroundColor Green 