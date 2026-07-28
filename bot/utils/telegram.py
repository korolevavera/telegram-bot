import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN", "")


def send_message(chat_id: int, text: str) -> None:
    if not BOT_TOKEN:
        print("BOT_TOKEN is not set, so the message was not sent")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    try:
        requests.post(url, json=payload, timeout=5)
    except requests.RequestException as exc:
        print(f"Failed to send message: {exc}")
