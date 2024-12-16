from flask import Flask, render_template, jsonify
from flask_mqtt import Mqtt
from collections import deque
import requests
from decryption_algo import decrypt_msg  # Import the decrypt_msg function

app = Flask(__name__)

# Flask-MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'mosquitto'  # Service name from Docker Compose
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0  # seconds

mqtt = Mqtt(app)

# Store sensor data for each device
sensor_data_device_1 = deque(maxlen=100)
sensor_data_device_2 = deque(maxlen=100)

TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
TELEGRAM_CHAT_ID = 'your_telegram_chat_id'

@app.route('/')
def index():
    return render_template('chart.html')

@app.route('/data')
def data():
    return jsonify({
        'device_1': list(sensor_data_device_1),
        'device_2': list(sensor_data_device_2)
    })

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        mqtt.subscribe('sensor/data')
    else:
        print(f"Failed to connect to MQTT broker, return code {rc}")
        send_telegram_alert(f"Failed to connect to MQTT broker, return code {rc}")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    print(f"Received payload: {payload}")  # Debugging line

    try:
        # Decrypt the payload
        decrypted_payload = decrypt_msg(payload)
        print(f"Decrypted payload: {decrypted_payload}")  # Debugging line

        # Determine the device and append to the corresponding deque
        if 'Device 1' in decrypted_payload:
            sensor_data_device_1.append(decrypted_payload)
        elif 'Device 2' in decrypted_payload:
            sensor_data_device_2.append(decrypted_payload)
        print(f"Appended data: {decrypted_payload}")  # Debugging line

    except ValueError as e:
        print(f"Error processing payload: {e}")
        send_telegram_alert(f"Error processing payload: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        send_telegram_alert(f"Unexpected error: {e}")

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
