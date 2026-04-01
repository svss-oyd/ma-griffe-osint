import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home(): return "ALIVE"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

async def hunt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /hunt pseudo")
        return
    
    user = context.args[0]
    await update.message.reply_text(f"⚡ Scan rapide de {user}...")
    
    # Commande socialscan (plus rapide que Sherlock)
    cmd = f"socialscan {user} --json"
    process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if process.stdout:
        await update.message.reply_text(f"✅ Résultats pour {user} :\n\n{process.stdout[:1000]}")
    else:
        await update.message.reply_text("⚠️ Aucun résultat trouvé ou serveur saturé.")

if __name__ == '__main__':
    Thread(target=run).start()
    token = os.getenv("TOKEN")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("hunt", hunt))
    application.run_polling()
