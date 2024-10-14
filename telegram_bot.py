import os
import subprocess
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Your bot token from BotFather
BOT_TOKEN = os.getenv('BOT_TOKEN')  # Fetch the bot token from environment variables

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /download <m3u8_url> to download and decrypt the video.")

def fetch_key_iv(video_key_url):
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

def download_video(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("Usage: /download <m3u8_url>")
        return

    m3u8_url = context.args[0]
    video_key_url = f"https://madxabhi-pw-78ab681aba3f.herokuapp.com/appx-hls-key?videoKey={m3u8_url}"

    key, iv = fetch_key_iv(video_key_url)

    if key and iv:
        # Assuming N_m3u8DL-RE is installed and in your PATH
        command = [
            'N_m3u8DL-RE', 
            '--key', key,
            '--iv', iv,
            m3u8_url
        ]

        try:
            subprocess.run(command, check=True)
            update.message.reply_text("Download completed! Uploading video...")
            
            # Assuming the output video file is named "output.mp4"
            # Modify this if the output filename is different
            output_file = "output.mp4"  # Change this to match the actual output filename

            # Upload the video to Telegram
            with open(output_file, 'rb') as video_file:
                update.message.reply_video(video_file)

            update.message.reply_text("Video uploaded successfully!")

        except subprocess.CalledProcessError as e:
            update.message.reply_text(f"Error during download: {e}")
    else:
        update.message.reply_text("Failed to retrieve key and IV.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("download", download_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
