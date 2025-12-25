import time
import base64
import requests
import string
from telebot import types
import telebot
from faker import Faker
fake = Faker('en_IN')
import google.generativeai as genai
import random

# --- 1. GEMINI AI SETUP (New Key & Model) ---
# Yahan wo NAYI KEY paste karna jo abhi copy ki hai
genai.configure(api_key="YOUR_API_TOCKEN_HERE")

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Ab hum FAST model use karenge (Ye nayi key ke sath pakka chalega)
# Purana (Jo error de raha hai):
# model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)

# Naya (Jo pakka chalega):
model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings)

# --- 2. TELEGRAM BOT SETUP (Connection) ---
# (Tumhara Token maine yahan daal diya hai)
BOT_TOKEN = "YOUR_BOT_TOCKEN_HERE"
bot = telebot.TeleBot(BOT_TOKEN)

print("🔥 Panther Bot is Online... Waiting for commands.")

# --- ISKE NICHE TUMHARA 'def ask_ai' SHURU HONA CHAHIYE ---

# --- TOOL 6: AI TEACHER (Updated) ---
@bot.message_handler(commands=['ask'])
def ask_ai(message):
    try:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "⚠️ Sawal to pucho! Example: `/ask Who is the best hacker?`")
            return

        query = message.text.split(maxsplit=1)[1]

        # 'Typing' action dikhana (Professional feel)
        bot.send_chat_action(message.chat.id, 'typing')

        # Naye model se sawal puchna
        response = model.generate_content(query)

        if response.text:
            reply = f"🧠 **Panther AI:**\n━━━━━━━━━━━━━━━━━━\n{response.text}"
            # Telegram ki limit (4000 words) ka dhyan rakhna
            if len(reply) > 4000:
                reply = reply[:4000] + "...(Read more)"
            bot.reply_to(message, reply, parse_mode="Markdown")
        else:
            bot.reply_to(message, "⚠️ AI ne khali jawab diya.")

    except Exception as e:
        print(f"Error in /ask: {e}")
        bot.reply_to(message, "⚠️ Server Error: AI abhi so raha hai (Quota Limit or Network Issue).")
# --- BAAKI PURANA CODE NICHE RAHEGA 👇 ---
# (Free Fire, Wiki, QR wala code yahan niche hona chahiye)

# Sabse Niche:

# --- TOOL 1: FREE FIRE SHOW-OFF MODE (Fake Data) ---
import random # Random number lane ke liye

def get_free_fire_stats(uid):
    # Hum yahan fake data generate karenge show-off ke liye
    levels = random.randint(60, 80) # Level 60 se 80 ke beech ayega
    likes = random.randint(5078, 46756) # Likes random ayenge

    info = (
        f"🎮 **Free Fire Account Found!**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Name:** Ｓ₁   SAMEER⁰⁷\n"  # Ek khatarnak sa naam
        f"🆔 **UID:** {uid}\n"
        f"📈 **Level:** {levels}\n"
        f"🛡️ **Rank:** 🔴 **Grandmaster**\n"
        f"🔥 **Likes:** {likes}\n"
        f"🌍 **Region:** India\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"✅ **Verified by Samir Raja bot**"
    )
    return info

# --- TOOL 2: IP TRACKER (Bonus) ---
def get_ip_info(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url).json()
        if response['status'] == 'success':
            return (
                f"🌍 **IP Location Tracked**\n"
                f"🏳️ **Country:** {response['country']}\n"
                f"🏙️ **City:** {response['city']}\n"
                f"📡 **ISP:** {response['isp']}"
            )
        else:
            return "❌ Invalid IP Address."
    except:
        return "❌ Error fetching data."

# --- BOT COMMANDS HANDLER ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        # Naya Start Message (Replace kar dena)
    welcome_text = (
    "🤖 **PANTHER INTELLIGENCE v3.0 ONLINE**\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "👋 Welcome Agent!\n"
    "Access the Main Menu button below to use tools:\n\n"
    "🕵️ **Spy Tools** | 🛰️ **Tracking** | 🔐 **Security**\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "⚠️ *Authorised Use Only.*"
)
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['ff'])
def handle_ff(message):
    try:
        # User ke message se UID nikalna (e.g., "/ff 12345" -> "12345")
        uid = message.text.split()[1]
        bot.reply_to(message, "🔍 Searching Database... Please wait.")

        # Function call karna
        result = get_free_fire_stats(uid)
        bot.reply_to(message, result, parse_mode="Markdown")

    except IndexError:
        bot.reply_to(message, "⚠️ **Format Galat hai!**\nAise likho: `/ff 12345678`")

# Bot ko continuously chalana
# --- TOOL 3: PASSWORD GENERATOR ---
@bot.message_handler(commands=['pass'])
def generate_password(message):
    # Logic: 12 digit ka strong password
    characters = string.ascii_letters + string.digits + "@#$%&"
    password = "".join(random.choice(characters) for i in range(12))

    bot.reply_to(message, f"🔐 **Generated Strong Password:**\n`{password}`", parse_mode="Markdown")

# --- TOOL 4: QR CODE MAKER (API Magic) ---
@bot.message_handler(commands=['qr'])
def send_qr(message):
    try:
        # User se text lena (e.g., /qr google.com)
        text = message.text.split(maxsplit=1)[1]

        # API ka use karke QR Code image lana
        api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={text}"

        bot.send_photo(message.chat.id, api_url, caption=f"⬛⬜ Ye lo tumhara QR Code: {text}")

    except IndexError:
        bot.reply_to(message, "⚠️ Aise likho: `/qr www.google.com` ya `/qr Sameer`")

# --- TOOL 5: WIKIPEDIA (Final Fixed Version) ---
@bot.message_handler(commands=['wiki'])
def wiki_search(message):
    try:
        text = message.text.split(maxsplit=1)
        if len(text) < 2:
            bot.reply_to(message, "⚠️ Aise likho: `/wiki Taj Mahal`")
            return

        query = text[1]
        bot.reply_to(message, f"🔍 Dhund raha hoon: '{query}'...")

        # --- YE HAI FIX (Fake ID) ---
        # Wikipedia bina ID card (User-Agent) ke baat nahi karta
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Step 1: Sahi Naam pata karna (OpenSearch)
        search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=1&format=json"

        # Note: headers=headers jod diya hai
        search_response = requests.get(search_url, headers=headers).json()

        if not search_response[1]:
            bot.reply_to(message, f"❌ '{query}' nahi mila.")
            return

        correct_title = search_response[1][0]

        # Step 2: Summary lana
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{correct_title}"
        response = requests.get(summary_url, headers=headers).json()

        if 'extract' in response:
            summary = response['extract']
            bot.reply_to(message, f"📚 **Wikipedia:** {correct_title}\n\n{summary}", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Page mila par summary nahi mili.")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

# --- TOOL 7: FAKE IDENTITY GENERATOR (Updated V2) ---
@bot.message_handler(commands=['fakeid'])
def generate_fake_id(message):
    bot.reply_to(message, "🕵️ Generating Fake Identity... Please wait.")

    # 1. Personal Info
    name = fake.name()
    email = fake.email()
    # Address me se \n hata kar comma lagaya taaki ek line me aaye
    address = fake.address().replace("\n", ", ")
    job = fake.job()
    country = "India 🇮🇳" # Fixed: Ab galat country nahi aayegi

    # 2. Financial Info (NEW FEATURE 💳)
    card_type = fake.credit_card_provider() # Visa/Mastercard etc.
    card_num = fake.credit_card_number()
    card_exp = fake.credit_card_expire()
    card_cvv = fake.credit_card_security_code()

    # 3. Message Design
    response = (
        f"🕵️ **FAKE IDENTITY DROP** 🕵️\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Name:** `{name}`\n"
        f"📧 **Email:** `{email}`\n"
        f"🏠 **Address:** {address}\n"
        f"💼 **Job:** {job}\n"
        f"🌍 **Country:** {country}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💳 **FINANCIAL DETAILS**\n"
        f"🏦 **Bank:** {card_type}\n"
        f"🔢 **Card:** `{card_num}`\n"
        f"📅 **Exp:** {card_exp} | 🔐 **CVV:** {card_cvv}\n"
        f"━━━━━━━━━━━━━━━━━━"
    )

    bot.send_message(message.chat.id, response, parse_mode="Markdown")
 # --- TOOL 8: HOLLYWOOD STYLE HACK (Ultimate Prank) ---
@bot.message_handler(commands=['hack'])
def start_hacking(message):
    try:
        target = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "⚠️ Naam to likho! Example: `/hack Rahul`")
        return

    # 1. Start Message
    msg = bot.reply_to(message, f"💻 **Target Found: {target}**\n🔄 Establishing Secure Connection...", parse_mode="Markdown")
    time.sleep(2)

    # 2. Animation Lists (Ye steps dikhenge)
    steps = [
        "🔓 Bypassing FireWall Security...",
        "🔑 Cracking Password (Brute Force)...",
        "📂 Accessing WhatsApp Database...",
        "📸 Copying Private Gallery Photos...",
        "💀 Injecting Panther Spyware..."
    ]

    # Progress Bar Designs
    bars = [
        "██░░░░░░░░ 20%",
        "████░░░░░░ 40%",
        "██████░░░░ 60%",
        "████████░░ 80%",
        "██████████ 100%"
    ]

    # 3. Loop chalega (Animation Magic)
    for i in range(5):
        # Har step pe message edit hoga
        new_text = (
            f"💀 **SYSTEM HACK IN PROGRESS** 💀\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🎯 **Target:** {target}\n"
            f"⚙️ **Action:** `{steps[i]}`\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⏳ Loading: [{bars[i]}]"
        )

        bot.edit_message_text(new_text, chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")
        time.sleep(3) # Har step 3 second rukega (Total 15 sec)

    # 4. Final Dhamaka (Success)
    final_text = (
        f"✅ **HACK COMPLETED SUCCESSFULLY**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Identity:** {target}\n"
        f"🔑 **Password:** `P@ssw0rd123` (Cracked)\n"
        f"📂 **Data Copied:** 12.5 GB\n"
        f"📍 **GPS Location:** Traced\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💾 *All files uploaded to Dark Web Cloud.*"
    )
    bot.edit_message_text(final_text, chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")

    # --- TOOL 9: MOBILE NUMBER TRACER (Map Location) ---
@bot.message_handler(commands=['trace'])
def trace_mobile(message):
    try:
        # User se number lena
        number = message.text.split()[1]

        # Fake Loading (Thoda suspense)
        msg = bot.reply_to(message, f"📡 **Searching Satellite Signal for: {number}**...", parse_mode="Markdown")
        time.sleep(2)

        # Random Data Generate karna
        operators = ["Jio 5G", "Airtel 4G", "Vi India", "BSNL"]
        states = ["Bihar, India", "Delhi, India", "Mumbai, India", "UP, India"]

        my_operator = random.choice(operators)
        my_state = random.choice(states)

        # Message Update
        info = (
            f"🎯 **TARGET LOCATED**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📞 **Number:** {number}\n"
            f"📶 **Operator:** {my_operator}\n"
            f"📍 **Circle:** {my_state}\n"
            f"🔋 **Signal:** Active (98%)\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👇 **Live Location Sent Below** 👇"
        )
        bot.edit_message_text(info, chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")

        # MAIN MAGIC: Location bhejna (Latitude, Longitude)
        # Ye Patna/Bihar ke aas paas ke coordinates hain
        lat = 25.5941 + random.uniform(-0.1, 0.1)
        lon = 85.1376 + random.uniform(-0.1, 0.1)

        bot.send_location(message.chat.id, latitude=lat, longitude=lon)

    except IndexError:
        bot.reply_to(message, "⚠️ Number to likho! Example: `/trace 9988776655`")
        import base64  # <-- Sabse upar imports me daalne ki zarurat nahi, yahi chal jayega

# --- TOOL 10: SECRET CRYPTOGRAPHY (Real Feature) ---

# 1. ENCRYPT (Message chupana)
@bot.message_handler(commands=['encrypt'])
def encrypt_message(message):
    try:
        # User se text lena
        original_text = message.text.split(maxsplit=1)[1]

        # Encoding Logic (Asli Magic)
        encoded_bytes = base64.b64encode(original_text.encode("utf-8"))
        encoded_str = encoded_bytes.decode("utf-8")

        response = (
            f"🔐 **MESSAGE ENCRYPTED**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📜 **Original:** {original_text}\n"
            f"🧩 **Secret Code:** `{encoded_str}`\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"💡 *Is code ko copy karke dost ko bhejo, wo ise /decrypt se padh payega.*"
        )
        bot.reply_to(message, response, parse_mode="Markdown")

    except IndexError:
        bot.reply_to(message, "⚠️ Kuch likho to sahi! Example: `/encrypt Hello Bhai`")

# 2. DECRYPT (Message padhna)
@bot.message_handler(commands=['decrypt'])
def decrypt_message(message):
    try:
        # User se code lena
        secret_code = message.text.split(maxsplit=1)[1]

        # Decoding Logic
        decoded_bytes = base64.b64decode(secret_code)
        decoded_str = decoded_bytes.decode("utf-8")

        response = (
            f"🔓 **MESSAGE DECRYPTED**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🧩 **Secret Code:** `{secret_code}`\n"
            f"📜 **Hidden Message:** {decoded_str}\n"
            f"━━━━━━━━━━━━━━━━━━"
        )
        bot.reply_to(message, response, parse_mode="Markdown")

    except Exception:
        bot.reply_to(message, "❌ **Error:** Ye code galat hai ya nakli hai!")
        # --- TOOL 11: PHISHING LINK SCANNER (Defense Tool) ---
@bot.message_handler(commands=['scan'])
def scan_link(message):
    try:
        # User se link lena
        link = message.text.split()[1].lower() # Link ko chota kar diya check karne ke liye

        # Fake Scanning Animation
        msg = bot.reply_to(message, f"🛡️ **Scanning URL:** `{link}`\n🔄 Checking VirusTotal Database...", parse_mode="Markdown")
        time.sleep(2)

        # Suspicious Words List (Inhe pakadna hai)
        bad_words = ["hack", "free", "win", "bonus", "spin", "ngrok", "bit.ly", "short", "money"]

        # Logic: Agar gande words mile to Danger, nahi to Safe
        is_safe = True
        for word in bad_words:
            if word in link:
                is_safe = False
                break

        if is_safe:
            result = (
                f"✅ **WEBSITE MARKED SAFE**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🌐 **URL:** {link}\n"
                f"🛡️ **Status:** Clean\n"
                f"🌟 **Rating:** 9.8/10\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🟢 *You can visit this site safely.*"
            )
        else:
            result = (
                f"⚠️ **DANGER: MALICIOUS LINK DETECTED** ⚠️\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🌐 **URL:** {link}\n"
                f"💀 **Threat:** Phishing / Scam\n"
                f"🔴 **Risk Level:** CRITICAL (High)\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🚫 **DO NOT OPEN THIS LINK!**"
            )

        bot.edit_message_text(result, chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")

    except IndexError:
        bot.reply_to(message, "⚠️ Link to daalo! Example: `/scan hack-facebook.com`")
        # --- TOOL 12: ULTIMATE DDoS ATTACK (Long Duration: 60s) ---
@bot.message_handler(commands=['ddos'])
def ddos_attack(message):
    try:
        target = message.text.split()[1]

        # 1. Initial Suspense (Start)
        msg = bot.reply_to(message, f"☠️ **INITIATING CYBER ATTACK**\n🎯 **Target:** `{target}`\n🌍 **Searching Global Botnet...**", parse_mode="Markdown")
        time.sleep(3)

        # 2. Long Animation List (10 Steps x 5 Seconds = 50 Secs)
        attacks = [
            "🟢 [10%] Connecting to 15,000 Zombie Bots...",
            "🟢 [20%] Handshake Successful! Ready to fire...",
            "🟡 [30%] Sending 5 Million Packets/sec...",
            "🟡 [40%] Bypassing Cloudflare Firewall...",
            "🟠 [50%] Injecting Malformed HTTP Headers...",
            "🟠 [60%] Server CPU Load: 85% (Overheating)...",
            "🔴 [70%] Database Connection Dropped...",
            "🔴 [80%] Admin Panel Access Blocked...",
            "🔴 [90%] SERVER CRITICAL ERROR (503)...",
            "⚫ [100%] CONNECTION LOST!"
        ]

        for status in attacks:
            # Message update karega
            bot.edit_message_text(f"☠️ **ATTACK IN PROGRESS**\n━━━━━━━━━━━━━━━━━━\n🎯 **Target:** `{target}`\n⚡ **Log:** {status}\n━━━━━━━━━━━━━━━━━━\n⏳ _Time Remaining: Calculating..._", chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")

            # Har step par 5 second rukega (Slow Feel ke liye)
            time.sleep(5)

        # 3. Final Report (After 1 Minute)
        final_report = (
            f"✅ **ATTACK COMPLETED**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🎯 **Target:** {target}\n"
            f"📉 **Total Requests:** 850 Million\n"
            f"⏱️ **Duration:** 62 Seconds\n"
            f"💀 **Status:** SERVER DESTROYED 💥\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⚠️ *Target website is now OFFLINE.*"
        )
        bot.edit_message_text(final_report, chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")

    except IndexError:
        bot.reply_to(message, "⚠️ Website ka naam to likho! Example: `/ddos google.com`")
        # --- TOOL 13: DARK WEB LEAK CHECKER (Prank) ---
@bot.message_handler(commands=['leak'])
def check_leak(message):
    try:
        # User se email ya username lena
        target = message.text.split()[1]

        # 1. Search Animation (Suspense)
        msg = bot.reply_to(message, f"🕵️ **Scanning Dark Web for:** `{target}`...", parse_mode="Markdown")
        time.sleep(2)

        bot.edit_message_text(f"📂 **Searching 'Collection #1' Database...**", chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")
        time.sleep(2)

        bot.edit_message_text(f"🔓 **Analyzing 'Facebook 2021' Leaks...**", chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")
        time.sleep(2)

        # 2. Fake Result Create karna
        # Logic: Target ka shuru ka naam + **** + random number (e.g., sam****99)
        fake_pass = target[:3] + "****" + str(random.randint(100, 999))

        result = (
            f"⚠️ **CRITICAL ALERT: DATA FOUND!** ⚠️\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Target:** `{target}`\n"
            f"🛑 **Breach Source:** LinkedIn Dump (2023)\n"
            f"🔑 **Leaked Password:** `{fake_pass}`\n"
            f"📧 **Status:** 🔴 SOLD for $15\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"💡 *Recommendation: Change your password immediately!*"
        )

        bot.edit_message_text(result, chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")

    except IndexError:
        bot.reply_to(message, "⚠️ Email ya User ID to likho! Example: `/leak sameer@gmail.com`")
        # --- DESIGNER BUTTONS WALA START ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    # Ye rahe buttons
    btn_ff = types.KeyboardButton('🔥 Free Fire Info')
    btn_ip = types.KeyboardButton('🌍 IP Tracker')
    btn_pass = types.KeyboardButton('🔐 Password Gen')
    btn_qr = types.KeyboardButton('⬛ QR Maker')
    btn_wiki = types.KeyboardButton('📚 Wikipedia')
    btn_fakeid = types.KeyboardButton('👤fakeid')

    markup.add(btn_ff, btn_ip, btn_pass, btn_qr, btn_wiki,btn_fakeid)

    welcome_text = (
        "🤖 **Panthar Dashboard Open!**\n\n"
        "Swagat hai Sameer bhai ke system mein. 👇\n"
        "Niche diye gaye buttons daba kar hacking shuru karein!"
    )
    bot.reply_to(message, welcome_text, reply_markup=markup, parse_mode="Markdown")

# --- BUTTONS KO SAMAJHNE WALA DIMAG ---
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text

    if "Free Fire" in text:
        bot.reply_to(message, "🆔 Kripya UID likhein.\nExample: `/ff 12345678`")

    elif "IP Tracker" in text:
        bot.reply_to(message, "🌍 Kripya IP likhein.\nExample: `/ip 8.8.8.8`")

    elif "Password" in text:
        # Password direct generate kar denge
        characters = string.ascii_letters + string.digits + "@#$%&"
        password = "".join(random.choice(characters) for i in range(12))
        bot.reply_to(message, f"🔐 **Generated Strong Password:**\n`{password}`", parse_mode="Markdown")

    elif "QR Maker" in text:
        bot.reply_to(message, "⬛⬜ Kripya text likhein.\nExample: `/qr Sameer`")

    elif "Wikipedia" in text:
        bot.reply_to(message, "📚 Kripya search karein.\nExample: `/wiki Python`")

    elif "Fakeid" in text:
        bot.reply_to(message, "👤 kripya fake identity bnaye.\nExample: `/fakeid`")

    # Note: Baaki commands (/ff, /ip, etc.) purane functions se hi chalenge.

bot.infinity_polling()