import os
import subprocess
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from flask import Flask
from threading import Thread

# --- SERVEUR WEB ---
app = Flask(__name__)
@app.route('/')
def index(): return "KALI CLAW ONLINE"
def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- MENU ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🕵️ SHERLOCK (Scan complet)", callback_data='scan_sherlock')],
                [InlineKeyboardButton("❌ ANNULER", callback_data='cancel')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = "
http://googleusercontent.com/immersive_entry_chip/0
http://googleusercontent.com/immersive_entry_chip/1
http://googleusercontent.com/immersive_entry_chip/2
