import requests
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    RAILWAY_URL = os.getenv("RAILWAY_URL", "")
    
    if not BOT_TOKEN:
        print("❌ Ошибка: BOT_TOKEN не найден в файле .env")
        return
        
    if not RAILWAY_URL:
        RAILWAY_URL = input("Введите URL вашего проекта на Railway (например: https://my-bot.up.railway.app): ").strip()
    
    webhook_url = f"{RAILWAY_URL.rstrip('/')}/webhook"
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    
    try:
        response = requests.post(api_url, json={"url": webhook_url}, timeout=10)
        response.raise_for_status()
        
        if response.ok:
            print(f"✅ Вебхук успешно установлен!")
            print(f"   URL: {webhook_url}")
            print("   Теперь бот будет получать все сообщения из Telegram!")
        else:
            print(f"❌ Ошибка: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка подключения или HTTP-ошибка при установке вебхука: {str(e)}")
    except Exception as e:
        print(f"❌ Неизвестная ошибка при установке вебхука: {str(e)}")

if __name__ == "__main__":
    main()