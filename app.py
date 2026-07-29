import os
import requests
from urllib.parse import urlparse
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook") # Изменено на /webhook
print(f"[DEBUG] WEBHOOK_PATH после os.getenv: {WEBHOOK_PATH}")
PORT = int(os.getenv("PORT", "5000"))


def normalize_webhook_path(value: str) -> str:
    if not value:
        return "/webhook" # Изменено на /webhook

    parsed = urlparse(value)
    if parsed.scheme and parsed.netloc:
        return parsed.path or "/webhook" # Изменено на /webhook

    if not value.startswith("/"):
        return f"/{value}"

    return value


WEBHOOK_PATH = normalize_webhook_path(WEBHOOK_PATH)
print(f"[DEBUG] Итоговый WEBHOOK_PATH: {WEBHOOK_PATH}")


def send_message(chat_id: int, text: str) -> None:
    if not BOT_TOKEN:
        print("BOT_TOKEN не установлен, сообщение не будет отправлено.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status() # Вызовет исключение для HTTP ошибок
        print(f"Сообщение успешно отправлено: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке сообщения: {e}")


@app.get("/")
def index():
    return "Telegram bot is running"


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post(WEBHOOK_PATH)
def telegram_webhook():
    print(f"[DEBUG] Функция telegram_webhook вызвана для пути: {WEBHOOK_PATH}")
    data = request.get_json(silent=True, force=True) or {}
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if chat_id and text == "/start":
        if BOT_TOKEN:
            send_message(chat_id, "Привет! Я твой первый Telegram-бот на Flask.")
        else:
            print("BOT_TOKEN is not set, so the message was not sent")
    elif chat_id: # Добавим обработку других сообщений для отладки
        print(f"Получено сообщение от {chat_id}: {text}")
        # send_message(chat_id, f"Я получил ваше сообщение: {text}") # Можно раскомментировать для ответа на любое сообщение

    return jsonify({"ok": True, "message": "Webhook received"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
