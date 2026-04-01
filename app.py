import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home(): return "OK"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

async def hunt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /hunt pseudo")
        return
    
    username = context.args[0]
    await update.message.reply_text(f"Searching {username}...")
    
    # Utilise Sherlock
    subprocess.run(f"sherlock {username} --timeout 15 --output report.txt", shell=True)
    
    if os.path.exists("report.txt"):
        await update.message.reply_document(open("report.txt", "rb"))
        os.remove("report.txt")
    else:
        await update.message.reply_text("No results.")

if __name__ == '__main__':
    Thread(target=run).start()
    token = os.getenv("TOKEN")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("hunt", hunt))
    application.run_polling()
