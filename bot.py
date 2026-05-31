import os
import random
import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Token, Admin ID fi Telebirr kee
TOKEN = "8200095818:AAHGl2VtiKQbt3dA6Vg5UOVB4H0g7QyVUOI"
ADMIN_ID = 6271558160
TELEBIRR_NUMBER = "0924720606"

# ---- LINKII DATABASE NEON KEE ----
# HUBADHU: Bakka "STTI_PASSWORD_KEE_GALCHI" jedhutti password kee isa dhugaa galchi!
DATABASE_URL = "postgresql://neondb_owner:STTI_PASSWORD_KEE_GALCHI@ep-divine-morning-ap5ugbss-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# ---- RENDER PORT SERVER ----
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# ---- DATABASE QOPHEESSUU (POSTGRESQL) ----
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0.0
        )
    """)
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return 0.0

def update_balance(user_id, username, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, username, balance) 
        VALUES (%s, %s, 0.0)
        ON CONFLICT (user_id) DO NOTHING
    """, (user_id, username))
    
    cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (amount, user_id))
    conn.commit()
    conn.close()

init_db()

# ---- BOT ACTIONS ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    balance = get_balance(user.id)
    
    keyboard = [
        [
            InlineKeyboardButton("🟢 DEPOSIT (Galchuuf) 🟢", callback_data="deposit"),
            InlineKeyboardButton("🔴 WITHDRAW (Baasuuf) 🟢", callback_data="withdraw")
        ],
        [InlineKeyboardButton("🎮 Tapha Jalqabi (Play Game) 🎲", callback_data="play_menu")],
        [
            InlineKeyboardButton("🔵 CUSTOMER SERVICE 🟢", callback_data="customer_service"),
            InlineKeyboardButton("💳 Balance (Herrega Kee)", callback_data="check_balance")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🔴🔴🔴🔴🔴🔴🔴🔴\n"
        "⚪⚪⚪🌳⚪⚪⚪\n"
        "⚫⚫⚫⚫⚫⚫⚫⚫\n\n"
        "**[Afaan Oromoo]**\n"
        f"Baga Nagaan Dhuftan! Gara Bot tapha carraa keenyaatti.\n💰 **Balance keessan:** {balance} Birr\n\n"
        "**[አማርኛ]**\n"
        f"እንኳን በደህና መጡ! ወደ ጨዋታ ቦታችን።\n💰 **የአሁኑ ሂሳብዎ:** {balance} Birr"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user = query.from_user
    balance = get_balance(user.id)
    
    if query.data == "customer_service":
        await query.edit_message_text(
            "🔵 **CUSTOMER SERVICE / የደንበኞች አገልግሎት** 🟢\n\n"
            "Afaan Oromoo: Rakkina ykn gaaffii qabdan gadi kanaan Admin keenya qunnamaa: @solee_Wes\n\n"
            "አማርኛ: ማንኛውም አይነት ችግር ወይም ጥያቄ ካለዎት ባለቤቱን ያግኙ: @solee_Wes",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Gara Fuladuraatti", callback_data="back_main")]])
        )
    elif query.data == "check_balance":
        await query.edit_message_text(
            f"💳 **Herrega Kee / ሂሳብዎ:**\n\nHerrega keessan yeroo ammaa `{balance} Birr` dha.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Gara Fuladuraatti", callback_data="back_main")]])
        )
    elif query.data == "deposit":
        await query.edit_message_text(
            f"🟢 **DEPOSIT (Qarshii Galchuuf) 🟢**\n\n"
            f"1. Lakkoofsa **Telebirr** keenya: `{TELEBIRR_NUMBER}` irratti kaffalaa.\n"
            f"2. Fakkii (Screenshot) kaffaltii bot kanaaf ergaa."
        )
    elif query.data == "withdraw":
        if balance < 100:
            await query.edit_message_text(
                f"🔴 **WITHDRAW (Qarshii Baasuuf) 🟢**\n\n❌ Qarshii baasuuf xiqqaan **100 Birr** ta'uu qaba. Balance keessan `{balance} Birr` qofa.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Duubatti", callback_data="back_main")]])
            )
        else:
            await query.edit_message_text(
                f"🔴 **WITHDRAW (Qarshii Baasuuf) 🟢**\n\n⏩ Maqaa Bankii, Lakkoofsa fi Hamma qarshii baastan nuuf barreessaa."
            )
    elif query.data == "play_menu":
        keyboard = [
            [InlineKeyboardButton("🎲 Tapha 5 Birr (Carraa 5-25)", callback_data="game_5")],
            [InlineKeyboardButton("🎲 Tapha 15 Birr (Carraa 15-75)", callback_data="game_15")],
            [InlineKeyboardButton("🎲 Tapha 25 Birr (Carraa 25-150)", callback_data="game_25")],
            [InlineKeyboardButton("🔙 Gara Fuladuraatti", callback_data="back_main")]
        ]
        await query.edit_message_text("🎮 **Taphawwan Carraa Filadhu:**", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data.startswith("game_"):
        cost = int(query.data.split("_")[1])
        if balance < cost:
            await query.edit_message_text(
                f"❌ Tapha kanaaf {cost} Birr si barbaachisa. Balance kee `{balance} Birr` dha. Maaloo dura Deposit godhi.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🟢 Deposit", callback_data="deposit")]])
            )
            return
        update_balance(user.id, user.username, -cost)
        nums = [random.randint(1, 7) for _ in range(3)]
        if cost == 5: win_amount = random.randint(5, 25)
        elif cost == 15: win_amount = random.randint(15, 75)
        else: win_amount = random.randint(25, 150)
        update_balance(user.id, user.username, win_amount)
        new_bal = get_balance(user.id)
        result_text = (
            f"🎲 **Bu'aa Carraa Kee:**\n\n🔢 Lakkoofsota: **{nums[0]} - {nums[1]} - {nums[2]}**\n"
            f"🎁 Badhaasa keessan: **+{win_amount} Birr** 🎉\n\n💳 Balance ammaa: `{new_bal} Birr`"
        )
        keyboard = [[InlineKeyboardButton("🔄 Ammas Taphadhu", callback_data=f"game_{cost}")], [InlineKeyboardButton("🔙 Menu", callback_data="back_main")]]
        await query.edit_message_text(result_text, reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "back_main":
        keyboard = [
            [InlineKeyboardButton("🟢 DEPOSIT (Galchuuf) 🟢", callback_data="deposit"), InlineKeyboardButton("🔴 WITHDRAW (Baasuuf) 🟢", callback_data="withdraw")],
            [InlineKeyboardButton("🎮 Tapha Jalqabi (Play Game) 🎲", callback_data="play_menu")],
            [InlineKeyboardButton("🔵 CUSTOMER SERVICE 🟢", callback_data="customer_service"), InlineKeyboardButton("💳 Balance (Herrega Kee)", callback_data="check_balance")]
        ]
        await query.edit_message_text(f"🔴⚪⚫ Balance: {balance} Birr", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_deposit_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    photo_file = update.message.photo[-1].file_id
    keyboard = [
        [InlineKeyboardButton("✅ Mirkaneessi (100)", callback_data=f"adm_dep_100_{user.id}")],
        [InlineKeyboardButton("✅ Mirkaneessi (500)", callback_data=f"adm_dep_500_{user.id}")],
        [InlineKeyboardButton("❌ Diduuf", callback_data=f"adm_rej_0_{user.id}")]
    ]
    await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo_file, caption=f"📩 Deposit: {user.first_name} (@{user.username})", reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text("🚀 Ragaan keessan Admin-itti ergameera!")

async def handle_text_requests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    text = update.message.text
    if user.id == ADMIN_ID: return
    keyboard = [
        [InlineKeyboardButton("✅ Baasii Mirkaneessi", callback_data=f"adm_wit_100_{user.id}")], 
        [InlineKeyboardButton("❌ Baasii Didu", callback_data=f"adm_rej_0_{user.id}")]
    ]
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 Withdraw Gaaffii:\n👤 Maamila: {user.first_name}\n📝 Odeeffannoo: {text}", reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text("🚀 Gaaffiin keessan Admin-itti ergameera.")

async def admin_verification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split("_")
    if len(parts) < 4: return
    
    _, req_type, amount, user_id = parts
    user_id = int(user_id)
    amount = float(amount)
    
    if req_type == "dep":
        update_balance(user_id, "", amount)
        msg_to_user = f"✅ Kaffaltiin keessan {amount} Birr mirkanaa'eera!"
        msg_to_admin = f"🟢 User ID {user_id} kaffaltii {amount} Birr mirkaneessitee jirta."
    elif req_type == "wit":
        msg_to_user = "✅ Gaaffiin qarshii baasuu keessan mirkanaa'eera!"
        msg_to_admin = f"🟢 User ID {user_id} Baasii isaa Mirkaneessitee jirta."
    else:
        msg_to_user = "❌ Dhiifama, gaaffiin keessan fudhatama hin arganne."
        msg_to_admin = f"🔴 User ID {user_id} Diddee jirta."
        
    try:
        await context.bot.send_message(chat_id=user_id, text=msg_to_user)
        await query.edit_message_text(text=msg_to_admin)
    except Exception: pass

def main():
    threading.Thread(target=run_health_server, daemon=True).start()
    
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click, pattern="^(deposit|withdraw|play_menu|check_balance|back_main|customer_service|game_.*)$"))
    application.add_handler(CallbackQueryHandler(admin_verification, pattern="^adm_"))
    application.add_handler(MessageHandler(filters.PHOTO, handle_deposit_receipt))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_requests))
    application.run_polling()

if __name__ == "__main__": 
    main()
