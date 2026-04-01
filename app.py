import os
import subprocess
from telegram.ext import Application, CommandHandler
from flask import Flask
from threading import Thread

# Config du serveur pour rester en ligne
app = Flask('')
@app.route('/')
def home(): return "Griffe Active"
def run_web(): app.run(host='0.0.0.0', port=8080)

# Commande de recherche
async def hunt(update, context):
    user = " ".join(context.args)
    if not user:
        await update.message.reply_text("❌ Mets un pseudo : /hunt [pseudo]")
        return
    await update.message.reply_text(f"🦅 La Griffe traque : {user}...")
    subprocess.run(f"maigret {user} --timeout 20 --output report.txt", shell=True)
    if os.path.exists("report.txt"):
        await update.message.reply_document(open("report.txt", "rb"))
    else:
        await update.message.reply_text("⚠️ Rien trouvé.")

# Lancement
if __name__ == '__main__':
    Thread(target=run_web).start()
    token = os.getenv("TOKEN")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("hunt", hunt))
    application.run_polling()
