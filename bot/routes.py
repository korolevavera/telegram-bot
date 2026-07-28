import os
from flask import request, jsonify
from bot import app
from bot.handlers.start_handler import handle_start

WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/telegram")

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
        handle_start(chat_id)

    return jsonify({"ok": True, "message": "Webhook received"})
