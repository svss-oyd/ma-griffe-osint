import os
import subprocess
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home(): return "SYSTEM ONLINE"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

async def hunt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Utilisation: /hunt pseudo")
        return
    
    username = context.args[0]
    await update.message.reply_text(f"🚀 Lancement de Sherlock sur : {username}...")
    
    try:
        # On force la sortie dans 'result.txt' pour être SUR de le trouver
        cmd = f"sherlock {username} --timeout 20 --output result.txt"
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # On vérifie si le fichier existe
        if os.path.exists("result.txt"):
            with open("result.txt", "rb") as file:
                await update.message.reply_document(document=file, filename=f"OSINT_{username}.txt", caption=f"🎯 Cible : {username}")
            os.remove("result.txt")
        else:
            # Si pas de fichier, on envoie ce que Sherlock a dit dans la console
            error_log = process.stdout if process.stdout else "Aucune réponse du système."
            await update.message.reply_text(f"⚠️ Rien trouvé ou erreur.\n\nLogs:\n`{error_log[:100]}`", parse_mode='Markdown')
            
    except Exception as e:
        await update.message.reply_text(f"💥 Erreur fatale : {str(e)}")

if __name__ == '__main__':
    Thread(target=run).start()
    token = os.getenv("TOKEN")
    if not token:
        print("ERREUR : Aucun TOKEN trouvé dans les variables d'environnement !")
    else:
        application = Application.builder().token(token).build()
        application.add_handler(CommandHandler("hunt", hunt))
        print("--- BOT DEMARRÉ ET PRET ---")
        application.run_polling()
