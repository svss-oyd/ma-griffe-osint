import os
import subprocess
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from flask import Flask
from threading import Thread

# --- SERVEUR FLASK ---
app = Flask(__name__)
@app.route('/')
def home(): return "KALI CLAW V2 ONLINE"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- COMMANDES ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🕵️ TRAQUER PSEUDO", callback_data='h')],
        [InlineKeyboardButton("🌐 INFOS IP", callback_data='i')],
        [InlineKeyboardButton("❌ ANNULER", callback_data='c')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("💀 *KALI CLAW V2*\nChoisissez une option :", reply_markup=reply_markup, parse_mode='Markdown')

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'h':
        context.user_data['choice'] = 'hunt'
        await query.edit_message_text("✍️ Envoie le **PSEUDO** à rechercher :")
    elif query.data == 'i':
        context.user_data['choice'] = 'ip'
        await query.edit_message_text("📍 Envoie l'adresse **IP** :")
    else:
        await query.edit_message_text("Annulé.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = context.user_data.get('choice')
    text = update.message.text

    if choice == 'hunt':
        await update.message.reply_text(f"🔎 Scan de {text}...")
        # On lance socialscan sans le mode JSON pour avoir un texte lisible
        cmd = f"socialscan {text} --show-all"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # On récupère le texte, si c'est vide on prévient l'utilisateur
        output = res.stdout.strip() if res.stdout else "Aucun résultat trouvé sur les réseaux majeurs."
        
        await update.message.reply_text(f"✅ Résultats pour {text} :\n\n{output[:1000]}")
    
    elif choice == 'ip':
        await update.message.reply_text(f"🌍 Analyse IP : {text}...")
        r = requests.get(f"http://ip-api.com/json/{text}").json()
        if r.get('status') == 'success':
            msg = f"📍 Ville: {r.get('city')}\n🏳️ Pays: {r.get('country')}\n🏢 ISP: {r.get('isp')}"
        else:
            msg = "❌ IP invalide."
        await update.message.reply_text(msg)
    
    context.user_data['choice'] = None

if __name__ == '__main__':
    Thread(target=run).start()
    token = os.getenv("TOKEN")
    app_tg = Application.builder().token(token).build()
    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(CallbackQueryHandler(button))
    app_tg.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app_tg.run_polling()
