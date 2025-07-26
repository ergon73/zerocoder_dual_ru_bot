# Настройка SSH доступа к VPS

**VPS IP:** your_vps_ip  
**Пользователь:** your_vps_user

## Ваши публичные SSH ключи

### Основной ключ (id_ed25519):
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... your_username
```

### Yandex Cloud ключ (yc_your_username_key):
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... your_username
```

## Инструкции по настройке

### 1. Подключитесь к VPS через веб-консоль или другой способ

### 2. Создайте папку .ssh и файл authorized_keys

```bash
# Создаем папку .ssh
mkdir -p ~/.ssh

# Создаем файл authorized_keys
touch ~/.ssh/authorized_keys

# Устанавливаем правильные права
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### 3. Добавьте ваш публичный ключ

Выполните одну из команд (в зависимости от того, какой ключ хотите использовать):

```bash
# Для основного ключа:
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... your_username" >> ~/.ssh/authorized_keys

# Или для Yandex Cloud ключа:
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... your_username" >> ~/.ssh/authorized_keys
```

### 4. Проверьте подключение

```bash
ssh your_vps_user@your_vps_ip
```

### Альтернативный способ (если у вас есть ssh-copy-id):

```bash
ssh-copy-id your_vps_user@your_vps_ip
```

### 5. Проверьте подключение еще раз

```bash
ssh your_vps_user@your_vps_ip
```

Если всё настроено правильно, вы должны подключиться без запроса пароля. 