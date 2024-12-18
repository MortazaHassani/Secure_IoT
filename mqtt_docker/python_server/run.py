# run.py
import threading
from app import app
from telegrambot import bot
import time

def run_flask():
    app.run(host='0.0.0.0', port=5000)

def run_telegram():
    bot.infinity_polling()

if __name__ == "__main__":
    # Create threads for Flask and Telegram bot
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    telegram_thread = threading.Thread(target=run_telegram, daemon=True)

    # Start both threads
    flask_thread.start()
    telegram_thread.start()

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
