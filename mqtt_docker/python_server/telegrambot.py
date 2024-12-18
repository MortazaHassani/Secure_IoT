import telebot
from telebot import types
import time
import threading
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Track user states (e.g., awaiting login input), login status, failed attempts, ban times, and message IDs
user_states = {}
logged_in_users = set()
failed_attempts = {}
banned_users = {}
message_ids = {}
update_threads = {}

# Welcome message and show keyboard
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Create the keyboard
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        types.KeyboardButton('login'),
        types.KeyboardButton('update'),
        types.KeyboardButton('chart'),
        types.KeyboardButton('logout')  # Add logout button
    ]
    markup.add(*buttons)

    # Send welcome message with the keyboard
    bot.send_message(message.chat.id, "Howdy, I am Vivi! How are you doing?\nChoose an option:", reply_markup=markup)

# Handle user button selections
@bot.message_handler(func=lambda message: message.text in ['login', 'update', 'chart', 'logout'])
def handle_options(message):
    chat_id = message.chat.id
    if message.text == 'login':
        if chat_id in banned_users and datetime.now() < banned_users[chat_id]:
            bot.send_message(chat_id, "You are temporarily banned. Try again later.")
        else:
            user_states[chat_id] = 'awaiting_password'  # Set state to awaiting password
            msg = bot.send_message(chat_id, "Please enter your login password:")
            message_ids[chat_id] = (message.message_id, msg.message_id)  # Store message IDs
    elif message.text == 'update':
        if chat_id in logged_in_users:
            if chat_id not in update_threads or not update_threads[chat_id].is_alive():
                bot.send_message(chat_id, "Starting updates... You will receive messages every 1 minute.")
                update_thread = threading.Thread(target=send_updates, args=(chat_id,), daemon=True)
                update_thread.start()
                update_threads[chat_id] = update_thread
            else:
                bot.send_message(chat_id, "Updates are already running.")
        else:
            bot.send_message(chat_id, "Please login first.")
    elif message.text == 'chart':
        if chat_id in logged_in_users:
            send_chart(chat_id)
        else:
            bot.send_message(chat_id, "Please login first.")
    elif message.text == 'logout':
        if chat_id in logged_in_users:
            logged_in_users.remove(chat_id)
            bot.send_message(chat_id, "You have been logged out.")
            stop_updates(chat_id)
            wipe_history(chat_id)
        else:
            bot.send_message(chat_id, "You are not logged in.")

# Handle password input for login
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_password')
def handle_password(message):
    chat_id = message.chat.id
    if message.text == 'yourpassword':  # Replace 'yourpassword' with the actual password
        logged_in_users.add(chat_id)
        bot.send_message(chat_id, "Login successful!")
        failed_attempts.pop(chat_id, None)  # Reset failed attempts
    else:
        failed_attempts[chat_id] = failed_attempts.get(chat_id, 0) + 1
        if failed_attempts[chat_id] >= 3:
            ban_time = datetime.now() + timedelta(hours=1)
            banned_users[chat_id] = ban_time
            bot.send_message(chat_id, "Too many failed attempts. You are banned for 1 hour.")
        else:
            bot.send_message(chat_id, "Incorrect password. Try again.")

    # Delete the login message and the bot's response
    user_msg_id, bot_msg_id = message_ids.pop(chat_id, (None, None))
    if user_msg_id:
        bot.delete_message(chat_id, user_msg_id)
    if bot_msg_id:
        bot.delete_message(chat_id, bot_msg_id)
    bot.delete_message(chat_id, message.message_id)

    user_states.pop(chat_id, None)  # Reset state

# Send updates every 1 minute
def send_updates(chat_id):
    for _ in range(10):  # Limit to 10 updates for demonstration
        if chat_id not in logged_in_users:
            break
        bot.send_message(chat_id, "This is an update message!")
        time.sleep(60)  # Wait 1 minute between messages

# Stop updates for a user
def stop_updates(chat_id):
    if chat_id in update_threads:
        update_threads[chat_id].do_run = False
        update_threads[chat_id].join()
        update_threads.pop(chat_id, None)

# Wipe history for a user
def wipe_history(chat_id):
    pass


# Send chart as an image
def send_chart(chat_id):
    # Send a static image (replace with a dynamic chart if needed)
    with open('chart.png', 'rb') as photo:  # Ensure 'chart.png' exists in your directory
        bot.send_photo(chat_id, photo, caption="Here is your chart!")

# Echo user messages (fallback)
@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def echo_all(message):
    bot.reply_to(message, message.text)

# Infinite polling to handle incoming messages
bot.infinity_polling()
