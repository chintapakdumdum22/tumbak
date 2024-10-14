import os
import subprocess
import requests
import asyncio
import signal
import threading  # Importing threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from LuciferBanker'


# Fetching the environment variables
API_ID = int(os.getenv("API_ID", "20736921"))
API_HASH = os.getenv("API_HASH", "42b34442e52dc3e07b3e0783389be8cb")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8015663864:AAGLRoTMXkj9Ndq4PL7oKLo0AtaYT68rxCM")
OWNER_ID = int(os.getenv("OWNER_ID", "1366730834"))
SUDO_USERS = list(map(int, os.getenv("SUDO_USERS", "1366730834").split()))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /download <m3u8_url> to download and decrypt the video.")

async def fetch_key_iv(video_key_url):
    try:
        response = requests.get(video_key_url)
        response.raise_for_status()
        data = response.json()
        key = data.get('key')  # Adjust based on your API response structure
        iv = data.get('iv')    # Adjust based on your API response structure
        return key, iv
    except Exception as e:
        print(f"Error fetching key and IV: {e}")
        return None, None

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /download <m3u8_url>")
        return

    m3u8_url = context.args[0]
    video_key_url = f"https://madxabhi-pw-78ab681aba3f.herokuapp.com/appx-hls-key?videoKey={m3u8_url}"

    key, iv = await fetch_key_iv(video_key_url)

    if key and iv:
        command = [
            'N_m3u8DL-RE', 
            '--key', key,
            '--iv', iv,
            m3u8_url
        ]

        try:
            subprocess.run(command, check=True)
            await update.message.reply_text("Download completed! Uploading video...")

            output_file = "output.mp4"  # Change this to match the actual output filename

            with open(output_file, 'rb') as video_file:
                await update.message.reply_video(video_file)

            await update.message.reply_text("Video uploaded successfully!")

        except subprocess.CalledProcessError as e:
            await update.message.reply_text(f"Error during download: {e}")
    else:
        await update.message.reply_text("Failed to retrieve key and IV.")

async def run_telegram_bot():
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("download", download_video))
    
    await bot_app.start()
    await bot_app.updater.start_polling()
    await bot_app.updater.idle()

def run_flask_app():
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))

def handle_exit(sig, frame):
    print("Shutting down gracefully...")
    asyncio.get_event_loop().stop()

def main():
    # Register shutdown handler
    signal.signal(signal.SIGINT, handle_exit)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, handle_exit)  # Handle termination signal

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    # Start the Telegram bot
    asyncio.run(run_telegram_bot())

if __name__ == '__main__':
    main()
