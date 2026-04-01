import os
import subprocess
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from flask import Flask
from threading import Thread

# --- SERVEUR DE MAINTIEN (POUR RENDER) ---
app = Flask(__name__)
@app.route('/')
def index(): return "KALI CLAW ONLINE"
def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- MENU STYLE KALI ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🦅 MAIGRET (Full Scan)", callback_data='scan_maigret')],
        [InlineKeyboardButton("🕵️ SHERLOCK (Classic)", callback_data='scan_sherlock')],
        [InlineKeyboardButton("🌐 SOCIALSCAN (Fast)", callback_data='scan_social')],
        [InlineKeyboardButton("❌ ANNULER", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_msg = (
        "```\n"
        "┌──(root💀kali-claw)-[~/osint]\n"
        "└─$ INITIALIZING PIVOT CONSOLE...\n"
        "--------------------------------\n"
        "SÉLECTIONNEZ VOTRE OUTIL DE FRAPPE :\n"
        "```"
    )
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode='MarkdownV2')

# --- GESTION DES BOUTONS ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'cancel':
        await query.edit_message_text("```\nOperation aborted.\n```", parse_mode='MarkdownV2')
        return

    context.user_data['tool'] = query.data
    await query.edit_message_text(f"
http://googleusercontent.com/immersive_entry_chip/0
http://googleusercontent.com/immersive_entry_chip/1
3.  **Sur Render :** Le déploiement va se relancer tout seul dès que tu auras sauvegardé sur GitHub.
4.  **Sur Telegram :** Tape la commande `/start`.

### 🕵️ Pourquoi c'est mieux ?
* **Look Kali :** Le texte s'affiche en mode "bloc de code" avec le prompt `root@kali`.
* **Pivot Facile :** Tu cliques sur le bouton, tu tapes le pseudo, et le bot s'occupe du reste.
* **Nettoyage :** Le bot supprime le rapport après l'envoi pour ne pas laisser de traces sur le serveur.

**Est-ce que tu veux que je rajoute d'autres outils dans le menu (genre recherche d'IP ou de mail) ?**
