import os
import json
import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from database import init_db, SessionLocal, User, Progress, encrypt_data, decrypt_data
from protocol_data import PROTOCOL

load_dotenv()
app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
PORT = int(os.getenv("PORT", "5000"))

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.get("/")
def index():
    return "Bot is running"

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/telegram") # Webhook путь
def webhook():
    data = request.get_json()
    msg = data.get("message", {})
    chat_id = str(msg.get("chat", {}).get("id"))
    text = msg.get("text", "")

    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=chat_id).first()
    
    # Если новый пользователь
    if not user:
        user = User(telegram_id=chat_id)
        session.add(user)
        session.commit()
        progress = Progress(telegram_id=chat_id, current_stage="diagnostic", current_step=0)
        session.add(progress)
        session.commit()
        send_message(chat_id, "Ты запустила Дневник Трансформаций! Отвечай цифрами от 1 до 5.")
    
    progress = session.query(Progress).filter_by(telegram_id=chat_id).first()
    
    # Если написали /start - начинаем сначала
    if text == "/start":
        progress.current_stage = "diagnostic"
        progress.current_step = 0
        progress.encrypted_answers = encrypt_data({})
        session.commit()
        stage_data = PROTOCOL[progress.current_stage]
        q = stage_data["questions"][0]
        send_message(chat_id, f"{q['text']}\n(Напиши цифру от 1 до 5)")
    else:
        # Сохраняем ответ
        current_answers = decrypt_data(progress.encrypted_answers)
        stage_data = PROTOCOL.get(progress.current_stage)
        
        if progress.current_stage in ["diagnostic", "level1"]:
            current_answers[str(progress.current_step)] = text
            progress.encrypted_answers = encrypt_data(current_answers)
            next_step = progress.current_step + 1
            
            if "days" in stage_data: # для уровней с днями
                total_questions = len(stage_data["days"][0]["questions"])
            else:
                total_questions = len(stage_data["questions"])
            
            if next_step >= total_questions:
                send_message(chat_id, f"✅ Этап '{progress.current_stage}' завершен. Скоро я подведу итог, а пока перехожу к следующему этапу!")
                # Логика перехода на уровень1 (упрощенно)
                progress.current_stage = "level1"
                progress.current_step = 0
                progress.encrypted_answers = encrypt_data({})
            else:
                progress.current_step = next_step
                if "days" in stage_data:
                    next_q = stage_data["days"][0]["questions"][next_step]
                else:
                    next_q = stage_data["questions"][next_step]
                send_message(chat_id, f"{next_q['text']}\n(Напиши цифру от 1 до 5)")
        
        session.commit()
    session.close()
    return jsonify({"ok": True})

if __name__ == "__main__":
    init_db()
    # Авто-вебхук
    railway_url = os.getenv("RAILWAY_PUBLIC_DOMAIN") or f"https://{os.getenv('RAILWAY_SERVICE_NAME')}.up.railway.app"
    if railway_url:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={railway_url}/telegram")
    app.run(host="0.0.0.0", port=PORT, debug=False)