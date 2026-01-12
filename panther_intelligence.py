"""
Project: Panther Intelligence Bot (v3.0)
Author: Samir Raja (Panther)
Description: Advanced Cybersecurity Simulation & Utility Bot integration with Gemini AI.
Note: Offensive tools (DDoS, Hack) are for EDUCATIONAL SIMULATION ONLY.
"""

import time
import base64
import requests
import string
import random
import logging
from telebot import types, TeleBot
from faker import Faker
import google.generativeai as genai

# --- CONFIGURATION ---
# [SECURITY WARNING]: Never commit real API Keys to GitHub. Use Environment Variables.
API_KEY_GEMINI = "YOUR_GEMINI_API_KEY_HERE"
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

# --- INITIALIZATION ---
genai.configure(api_key=API_KEY_GEMINI)
model = genai.GenerativeModel('gemini-pro')
fake = Faker('en_IN')

bot = TeleBot(BOT_TOKEN)

print(" [SYSTEM] Panther Intelligence v3.0 is Online...")

# --- 1. WELCOME & DASHBOARD ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    # Professional Dashboard Buttons
    btn_ai = types.KeyboardButton('🤖 Ask AI')
    btn_track = types.KeyboardButton('🌍 IP Tracer')
    btn_sec = types.KeyboardButton('🔐 Password Gen')
    btn_qr = types.KeyboardButton('⬛ QR Generator')
    btn_id = types.KeyboardButton('🕵️ Fake Identity')
    btn_sim = types.KeyboardButton('💀 Breach Sim')

    markup.add(btn_ai, btn_track, btn_sec, btn_qr, btn_id, btn_sim)

    welcome_text = (
        "🤖 **PANTHER INTELLIGENCE SYSTEM v3.0**\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👋 Welcome, Agent.\n"
        "This tool provides OSINT utilities and Cybersecurity Simulations.\n\n"
        "⚙️ **Operational Modules:**\n"
        "🔹 AI Assistant (Gemini Pro)\n"
        "🔹 Reconnaissance Tools (IP, Trace)\n"
        "🔹 Encryption & Security\n"
        "🔹 Attack Simulations (Educational)\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👇 *Select a module from the dashboard below:*"
    )
    bot.reply_to(message, welcome_text, reply_markup=markup, parse_mode="Markdown")

# --- 2. AI MODULE (Gemini) ---
@bot.message_handler(commands=['ask'])
def ask_ai(message):
    try:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "⚠️ **Syntax Error:** Usage: `/ask [Your Question]`")
            return

        query = message.text.split(maxsplit=1)[1]
        bot.send_chat_action(message.chat.id, 'typing')
        
        response = model.generate_content(query)
        
        if response.text:
            reply = f"🧠 **Panther AI Analysis:**\n━━━━━━━━━━━━━━━━━━\n{response.text}"
            if len(reply) > 4000: reply = reply[:4000] + "..."
            bot.reply_to(message, reply, parse_mode="Markdown")
        else:
            bot.reply_to(message, "⚠️ AI returned no data.")

    except Exception as e:
        bot.reply_to(message, f"⚠️ **System Error:** {e}")

# --- 3. RECONNAISSANCE TOOLS ---
@bot.message_handler(commands=['ip'])
def get_ip_info(message):
    try:
        ip = message.text.split()[1] if len(message.text.split()) > 1 else "8.8.8.8"
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url).json()
        
        if response['status'] == 'success':
            info = (
                f"🌍 **IP GEOLOCATION REPORT**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🏳️ **Country:** {response['country']}\n"
                f"🏙️ **City:** {response['city']}\n"
                f"📡 **ISP:** {response['isp']}\n"
                f"📍 **Coordinates:** {response['lat']}, {response['lon']}"
            )
            bot.reply_to(message, info, parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Invalid IP Address.")
    except:
        bot.reply_to(message, "⚠️ Usage: `/ip [Address]`")

# --- 4. SECURITY UTILITIES ---
@bot.message_handler(commands=['pass'])
def generate_password(message):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = "".join(random.choice(chars) for i in range(16))
    bot.reply_to(message, f"🔐 **High-Entropy Password:**\n`{password}`", parse_mode="Markdown")

@bot.message_handler(commands=['fakeid'])
def generate_fake_id(message):
    info = (
        f"🕵️ **SYNTHETIC IDENTITY GENERATED**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Name:** `{fake.name()}`\n"
        f"📧 **Email:** `{fake.email()}`\n"
        f"💼 **Occupation:** {fake.job()}\n"
        f"💳 **Credit Card:** {fake.credit_card_number()} (Visa)\n"
        f"📍 **Address:** {fake.address().replace(chr(10), ', ')}\n"
        f"━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, info, parse_mode="Markdown")

# --- 5. ENCRYPTION MODULE ---
@bot.message_handler(commands=['encrypt'])
def encrypt_message(message):
    try:
        text = message.text.split(maxsplit=1)[1]
        encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        bot.reply_to(message, f"🔐 **AES-256 (Simulated) Encryption:**\n`{encoded}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ Usage: `/encrypt [Message]`")

@bot.message_handler(commands=['decrypt'])
def decrypt_message(message):
    try:
        code = message.text.split(maxsplit=1)[1]
        decoded = base64.b64decode(code).decode("utf-8")
        bot.reply_to(message, f"🔓 **Decrypted Payload:**\n`{decoded}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Decryption Failed: Invalid Hash.")

# --- 6. OFFENSIVE SIMULATIONS (EDUCATIONAL ONLY) ---
@bot.message_handler(commands=['hack'])
def simulation_hack(message):
    try:
        target = message.text.split()[1]
        msg = bot.reply_to(message, f"☠️ **INITIATING BREACH PROTOCOL: {target}**", parse_mode="Markdown")
        
        steps = [
            "🔨 Bypassing Firewall (Port 443)...",
            "💉 Injecting SQL Payload...",
            "📂 Dumping Database Tables...",
            "🔑 Decrypting Admin Hashes...",
            "✅ Root Access Granted."
        ]
        
        for step in steps:
            time.sleep(1.5)
            bot.edit_message_text(f"☠️ **SYSTEM BREACH IN PROGRESS**\nTarget: `{target}`\n\n> {step}", 
                                  chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")
        
        bot.edit_message_text(f"✅ **OPERATION SUCCESSFUL**\nTarget `{target}` has been compromised.\nData uploaded to local server.", 
                              chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ Usage: `/hack [Username]`")

@bot.message_handler(commands=['ddos'])
def simulation_ddos(message):
    try:
        target = message.text.split()[1]
        msg = bot.reply_to(message, f"🚀 **ESTABLISHING BOTNET CONNECTION...**", parse_mode="Markdown")
        
        for i in range(10, 101, 20):
            time.sleep(1)
            bot.edit_message_text(f"🔥 **DDoS ATTACK SIMULATION**\nTarget: `{target}`\nPacket Load: {i} TB/s\n\n[|||||||||| {i}%]", 
                                  chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")
            
        bot.edit_message_text(f"💀 **SERVER OFFLINE**\nTarget `{target}` is unresponsive (503 Service Unavailable).", 
                              chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ Usage: `/ddos [Domain]`")

# --- 7. BUTTON HANDLER ---
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    txt = message.text
    if txt == '🤖 Ask AI':
        bot.reply_to(message, "💡 **AI Mode:** Type `/ask [Your Question]`")
    elif txt == '🌍 IP Tracer':
        bot.reply_to(message, "📡 **Trace Mode:** Type `/ip [IP Address]`")
    elif txt == '🔐 Password Gen':
        generate_password(message)
    elif txt == '🕵️ Fake Identity':
        generate_fake_id(message)
    elif txt == '💀 Breach Sim':
        bot.reply_to(message, "⚠️ **Warning:** Simulation Only.\nType `/hack [Name]` or `/ddos [URL]`")
    elif txt == '⬛ QR Generator':
        bot.reply_to(message, "usage: `/qr [Link]` (Feature under maintenance)")

# --- MAIN LOOP ---
if __name__ == "__main__":
    bot.infinity_polling()
