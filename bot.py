import os
import time
import requests
from flask import Flask
from telegram import Bot

app = Flask(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN', '8459761675:AAEqqjzhV3twVaxWF-d2UnT9MGcTLBwGTfc')
CHANNEL_ID = os.getenv('CHANNEL_ID', '@tonpricevery')

bot = Bot(BOT_TOKEN)

def send_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=TONUSDT"
        response = requests.get(url, timeout=5)
        price = float(response.json()['price'])
        
        message = f"${round(price, 4)}"
        bot.send_message(CHANNEL_ID, message, disable_notification=True)
        print(f"{time.strftime('%H:%M:%S')} ✅ {message}")
        return True
    except Exception as e:
        print(f"{time.strftime('%H:%M:%S')} ❌ {e}")
        return False

@app.route('/')
def home():
    send_price()
    return "TON Price Bot is running!"

@app.route('/send')
def send():
    if send_price():
        return "✅ Price sent to Telegram!"
    return "❌ Error sending price"

def bot_worker():
    """Фоновая задача отправки каждые 30 секунд"""
    while True:
        send_price()
        time.sleep(30)

if __name__ == "__main__":
    from threading import Thread
    
    # Запускаем фоновую задачу
    Thread(target=bot_worker, daemon=True).start()
    
    # Запускаем веб-сервер
    app.run(host='0.0.0.0', port=10000)
