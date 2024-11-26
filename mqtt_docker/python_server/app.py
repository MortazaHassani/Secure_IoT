from flask import Flask, render_template, jsonify
from flask_mqtt import Mqtt
import threading
from collections import deque
import requests

app = Flask(__name__)

# Flask-MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'mosquitto'  # Service name from Docker Compose
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0  # seconds

mqtt = Mqtt(app)

# Store sensor data
sensor_data = deque(maxlen=100)

# Telegram Bot Configuration
#TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
#TELEGRAM_CHAT_ID = "your-chat-id"

@app.route('/')
def index():
    return render_template('chart.html')

@app.route('/data')
def data():
    return jsonify(list(sensor_data))

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")  # Debugging line
    mqtt.subscribe('sensor/data')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    print(f"Received payload: {payload}")  # Debugging line
    try:
        sensor_data.append(float(payload))
        print(f"Appended data: {float(payload)}")  # Debugging line
    except ValueError as e:
        print(f"Error converting payload to float: {e}")

    # Send Telegram alert if a condition is met
    #if float(payload) > 50:  # Example threshold
        #send_telegram_alert(f"Sensor value high: {payload}")

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
