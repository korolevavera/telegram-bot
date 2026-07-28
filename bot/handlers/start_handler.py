from bot.utils.telegram import send_message


def handle_start(chat_id: int) -> None:
    send_message(chat_id, "Привет! Я твой первый Telegram-бот на Flask.")
