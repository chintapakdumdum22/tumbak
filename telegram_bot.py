import os
import subprocess
import requests
from flask import Flask, request
from telethon import TelegramClient, events
from pymongo import MongoClient
from threading import Thread

# Ensure the downloads directory exists
os.makedirs('./downloads', exist_ok=True)

# Environment variables with defaults
API_ID = os.getenv("API_ID", "20736921")
API_HASH = os.getenv("API_HASH", "42b34442e52dc3e07b3e0783389be8cb")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8015663864:AAGLRoTMXkj9Ndq4PL7oKLo0AtaYT68rxCM")
OWNER_ID = int(os.getenv("OWNER_ID", "1366730834"))
SUDO_USERS = list(map(int, os.getenv("SUDO_USERS", "1996039956").split(",")))
MONGO_URL = os.getenv("MONGO_DB", "mongodb+srv://creatorar30:fdINvMPYXYwUyHdq@cluster0.pbaou.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Initialize Telegram client
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# MongoDB setup
mongo_client = MongoClient(MONGO_URL)
db = mongo_client['telegram_bot_db']

# Flask app initialization
app = Flask(__name__)

# Extract URI and IV from the m3u8 link
def extract_uri_iv(m3u8_link):
    response = requests.get(m3u8_link)
    lines = response.text.split('\n')
    uri = None
    iv = None
    for line in lines:
        if line.startswith("#EXT-X-KEY"):
            uri = line.split('URI="')[1].split('"')[0]
            iv = line.split('IV=')[1] if 'IV=' in line else None
            break
    return uri, iv

# Get the decryption key using the provided API
def get_decryption_key(uri):
    key_url = f"https://madxabhi-pw-78ab681aba3f.herokuapp.com/appx-hls-key?videoKey={uri}"
    response = requests.get(key_url)
    return response.text

# Download and decrypt the m3u8 video using N_m3u8DL-RE
def download_and_decrypt(m3u8_link, key, iv):
    command = [
        "./N_m3u8DL-RE",  # Use relative path
        m3u8_link,
        "--key", key,
        "--iv", iv,
        "--save-dir", "./downloads",
        "--auto-select"
    ]
    subprocess.run(command, check=True)
    return './downloads/decrypted_video.mp4'

# Telegram Bot: Handle start command
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Send me an m3u8 link to download and decrypt.')

# Telegram Bot: Handle m3u8 link
@client.on(events.NewMessage)
async def handle_message(event):
    sender_id = event.sender_id
    print(f"Sender ID: {sender_id}")  # Debugging line
    if sender_id != OWNER_ID and sender_id not in SUDO_USERS:
        await event.reply("You are not authorized to use this bot.")
        return
    # ... rest of your code


    m3u8_link = event.text
    await event.reply("Processing your request...")

    try:
        # Extract URI and IV from m3u8 link
        uri, iv = extract_uri_iv(m3u8_link)
        if not uri or not iv:
            await event.reply("Failed to extract URI and IV from the m3u8 link.")
            return

        # Get decryption key
        key = get_decryption_key(uri)
        if not key:
            await event.reply("Failed to retrieve the decryption key.")
            return

        # Download and decrypt the video
        video_path = download_and_decrypt(m3u8_link, key, iv)
        await event.reply("Video downloaded and decrypted successfully. Uploading...")

        # Upload decrypted video to Telegram
        await client.send_file(event.chat_id, video_path, caption="Here is your decrypted video!")

    except Exception as e:
        await event.reply(f"An error occurred: {str(e)}")

# Flask health check route for Koyeb
@app.route('/')
def index():
    return 'Telegram bot is running.'

# Function to run the Flask app
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Start both Flask app and Telegram bot
if __name__ == '__main__':
    # Run Flask app in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Start Telegram client and listen for messages
    client.run_until_disconnected()
