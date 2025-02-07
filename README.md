# IMAI_bot

## Описание
Проект содержит в себе Telegram-бот и API с функционалом, предусматривающим отправку
запроса информации по IMEI устройства и получением информации об этом устройстве.

## Эндпоинты API

### Аутентификация

*   `POST` `http://imei.ddns.net/api/auth/signup/`
    *   **Описание:** Регистрация нового пользователя.
    *   **Параметры тела запроса (JSON):** `username`, `telegram_id`.
    *   **Ответ:**
        *   `201 Created`: Пользователь успешно зарегистрирован.
*   `POST` `http://imei.ddns.net/api/auth/token/`
    *   **Описание:** Получение JWT-токена.
    *   **Параметры тела запроса (JSON):** `username`, `telegram_id`.
    *   **Ответ:**
        *   `200 OK`: Успешная аутентификация, возвращается JWT-токен.
        *   `401 Unauthorized`: Неверные учетные данные.

### Функционал

*   `POST` `http://imei.ddns.net/api/check-imei/`
    *   **Описание:** Получение инормации об устройстве по IMEI.
    *   **Параметры тела запроса (JSON):** `imei`, `token`. IMEI устройства и TOKEN для аутентификации в стороннем сервисе.
    *   **Ответ:**
        *   `201 Created`: Информация об устройстве в формате JSON
