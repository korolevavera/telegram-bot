import os
import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/telegram")
PORT = int(os.getenv("PORT", "5000"))


def send_message(chat_id: int, text: str) -> None:
    if not BOT_TOKEN:
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload, timeout=5)


@app.get("/")
def index():
    return "Telegram bot is running"


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post(WEBHOOK_PATH)
def telegram_webhook():
    data = request.get_json(silent=True, force=True) or {}
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if chat_id and text == "/start":
        if BOT_TOKEN:
            send_message(chat_id, "Привет! Я твой первый Telegram-бот на Flask.")
        else:
            print("BOT_TOKEN is not set, so the message was not sent")

    return jsonify({"ok": True, "message": "Webhook received"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
