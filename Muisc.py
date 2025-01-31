from pyrogram import Client, filters
import os
import youtube_dl
from datetime import datetime, timedelta

# Bot Credentials
BOT_TOKEN = "7605439275:AAEs-ZhUfC9P-VV46EWZRB-hS67HQfVNVvw"  # Yahan apna bot token daal
ADMIN_ID = 6353114118 # Apna admin Telegram ID daal

# User Database (User ID -> Expiry Date)
users = {}

# Initialize Bot (No API_ID & API_HASH needed)
app = Client("mp3_downloader_bot", bot_token=BOT_TOKEN)

# 🔹 Download MP3 from Video
def download_audio(video_url):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": "downloads/%(title)s.%(ext)s",
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        return f"downloads/{info['title']}.mp3"

# 🔹 Admin Command to Add User
@app.on_message(filters.command("add") & filters.user(ADMIN_ID))
def add_user(client, message):
    try:
        _, user_id, days = message.text.split()
        user_id = int(user_id)
        days = int(days)
        expiry_date = datetime.now() + timedelta(days=days)
        users[user_id] = expiry_date
        message.reply_text(f"✅ User `{user_id}` added for {days} days (Till {expiry_date.date()}).")
    except:
        message.reply_text("❌ Format: `/add user_id days`")

# 🔹 Start Command
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("👋 Bhai! Mujhe koi bhi YouTube/Video ka link bhejo, main usko MP3 me convert karke dunga! 🎵")

# 🔹 Handle Video Link (Check User Access)
@app.on_message(filters.text & filters.private)
def convert_to_mp3(client, message):
    user_id = message.from_user.id
    if user_id not in users or users[user_id] < datetime.now():
        message.reply_text("❌ Bhai, tu authorized nahi hai. Admin se baat kar.")
        return
    
    video_url = message.text
    try:
        msg = message.reply_text("⏳ Downloading & Converting...")
        mp3_file = download_audio(video_url)
        message.reply_audio(audio=mp3_file, caption="✅ Yeh lo bhai, tumhara MP3! 🎶")
        os.remove(mp3_file)  # Clean up
        msg.delete()
    except Exception as e:
        message.reply_text(f"❌ Error: {str(e)}")

# 🔹 Start Bot
app.run()
