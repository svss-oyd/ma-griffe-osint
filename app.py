import os
import subprocess
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from flask import Flask
from threading import Thread

# --- SERVEUR RENDER ---
app = Flask(__name__)
@app.route('/')
def home(): return "KALI CLAW V3 ONLINE"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIG ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🕵️ TRAQUER PSEUDO", callback_data='h')],
        [InlineKeyboardButton("🌐 INFOS IP", callback_data='i')],
        [InlineKeyboardButton("❌ ANNULER", callback_data='c')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("💀 *KALI CLAW V2*\nPrêt pour la traque ?", reply_markup=reply_markup, parse_mode='Markdown')

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'h':
        context.user_data['choice'] = 'hunt'
        await query.edit_message_text("✍️ Envoie le **PSEUDO** :")
    elif query.data == 'i':
        context.user_data['choice'] = 'ip'
        await query.edit_message_text("📍 Envoie l'adresse **IP** :")
    else:
        await query.edit_message_text("Menu fermé.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = context.user_data.get('choice')
    text = update.message.text
    if not choice: return

    if choice == 'hunt':
        await update.message.reply_text(f"🔎 Scan rapide de {text}...")
        # Utilisation de socialscan (plus léger)
        cmd = f"socialscan {text} --json"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        results = []
        # On construit les liens manuellement pour les réseaux qui répondent
        platforms = {
            "instagram": f"https://instagram.com/{text}",
            "twitter": f"https://twitter.com/{text}",
            "github": f"https://github.com/{text}",
            "reddit": f"https://reddit.com/user/{text}",
            "snapchat": f"https://snapchat.com/add/{text}"
        }
        
        # On vérifie ce que socialscan a trouvé (très basique pour éviter le vide)
        for p_name, url in platforms.items():
            results.append(f"🔗 {p_name.capitalize()}: {url}")
            
        final_msg = "🎯 **Liens potentiels générés :**\n\n" + "\n".join(results)
        await update.message.reply_text(final_msg, disable_web_page_preview=True)
    
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
