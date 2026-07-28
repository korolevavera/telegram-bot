# Минимальный Telegram-бот на Flask

Это очень простой стартовый проект. Я уже подготовил всё, чтобы тебе было легче.

## Что делать

1. Открой папку проекта.
2. Скопируй `.env.example` в `.env` и вставь в него свой токен:
   ```env
   BOT_TOKEN=твой_токен
   WEBHOOK_PATH=/telegram
   ```
3. Запусти файл `install.bat`.
4. После установки запусти файл `start.bat`.
5. Открой браузер и перейди на:
   http://127.0.0.1:5000/

## Что в проекте
- `bot/` — основная папка бота
- `bot/routes.py` — маршруты Flask и обработка webhook
- `bot/utils/telegram.py` — отправка сообщений Telegram
- `app.py` — временный запуск для локальной проверки
- `wsgi.py` — запуск через Gunicorn на Railway
- `requirements.txt` — зависимости
- `Procfile` — команда старта на Railway
- `runtime.txt` — версия Python для Railway
- `mise.toml` — настройка Python attestation для Railway
- `install.bat` — установка зависимостей
- `start.bat` — запуск локально

## Для настоящего бота
1. Создай бота через @BotFather.
2. Вставь токен в файл `.env`:
   ```env
   BOT_TOKEN=твой_токен
   WEBHOOK_PATH=/telegram
   ```

## Если терминал ругается
Ошибка обычно связана не с тем, что ты сделал не так, а с тем, что команда была введена не из корня проекта или виртуальная среда не активирована.

## Развёртывание на Railway
1. Создай проект на Railway и подключи репозиторий.
2. Убедись, что в корне проекта есть файлы:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `mise.toml`
3. В настройках Railway добавь переменную окружения `BOT_TOKEN`.
4. После успешного деплоя подтверди webhook в Telegram, используя публичный URL проекта и путь `WEBHOOK_PATH`.

> Пример webhook: `https://<project-domain>/telegram`.
