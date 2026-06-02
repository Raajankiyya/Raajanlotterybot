import os
import random
import psycopg
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Token, Admin ID fi Telebirr kee
TOKEN = "8200095818:AAHGl2VtiKQbt3dA6Vg5UOVB4H0g7QyVUOI"
ADMIN_ID = 6271558160
TELEBIRR_NUMBER = "0924720606"

# DATABASE NEON
DATABASE_URL = "postgresql://neondb_owner:npg_3QVYKmcTG9Rn@ep-divine-morning-ap5ugbss-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# ---- SERVER FOR RENDER ----
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

# ---- DATABASE QUQQUNNAMTII ----
def get_db_connection():
    return psycopg.connect(DATABASE_URL)

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
    cursor.close()
    conn.close()

def get_balance(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return round(float(row[0]), 2)
    return 0.0

def update_balance(user_id, username, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, username, balance) 
        VALUES (%s, %s, 0.0)
        ON CONFLICT (user_id) DO UPDATE SET username = EXCLUDED.username
    """, (user_id, username))
    
    cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (amount, user_id))
    conn.commit()
    cursor.close()
    conn.close()

init_db()

# ---- BUTTON MAIN MENU ----
def get_main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🟢 DEPOSIT (Galchuuf) 🟢", callback_data="deposit"),
            InlineKeyboardButton("🔴 WITHDRAW (Baasuuf) 🟢", callback_data="withdraw")
        ],
        [InlineKeyboardButton("🎮 Tapha Jalqabi (Play Game) 🎲", callback_data="play_menu")],
        [
            InlineKeyboardButton("🔵 CUSTOMER SERVICE 🟢", callback_data="customer_service"),
            InlineKeyboardButton("💳 Balance (Herrega Kee)", callback_data="check_balance")
        ]
    ])

# ---- BOT ACTIONS ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    balance = get_balance(user.id)
    
    welcome_text = (
        "🔴🔴🔴🔴🔴🔴🔴🔴\n"
        "⚪⚪⚪🌳⚪⚪⚪\n"
        "⚫⚫⚫⚫⚫⚫⚫⚫\n\n"
        "[Afaan Oromoo]\n"
        f"Baga Nagaan Dhuftan! Gara Bot tapha carraa keenyaatti.\n💰 Balance keessan: {balance} Birr\n\n"
        "[አማርኛ]\n"
        f"እንኳን በደህና መጡ! ወደ ጨዋታ ቦታችን።\n💰 የአሁኑ ሂሳብዎ: {balance} Birr"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user = query.from_user
    balance = get_balance(user.id)
    
    if query.data == "customer_service":
        await query.edit_message_text(
            "🔵 CUSTOMER SERVICE / የደንበኞች አገልግሎት 🟢\n\n"
            "Afaan Oromoo: Rakkina ykn gaaffii qabdan gadi kanaan Admin keenya qunnamaa: @solee_Wes\n\n"
            "አማርኛ: ማንኛውም አይነት ችግር ወይም ጥያቄ ካለዎት ባለቤቱን ያግኙ: @solee_Wes",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Gara Main Menu", callback_data="back_main")]])
        )
    elif query.data == "check_balance":
        await query.edit_message_text(
            f"💳 Herrega Kee / ሂሳብዎ:\n\nHerrega keessan yeroo ammaa {balance} Birr dha.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Gara Main Menu", callback_data="back_main")]])
        )
    elif query.data == "deposit":
        await query.edit_message_text(
            f"🟢 DEPOSIT (Qarshii Galchuuf) 🟢\n\n"
            f"1. Lakkoofsa Telebirr keenya: {TELEBIRR_NUMBER} irratti kaffalaa.\n"
            f"2. Fakkii (Screenshot) kaffaltii ergaa.\n"
            f"💡 Hubachiisa: Screenshot yeroo ergitan gadi irratti hamma qarshii galchitan (Fkn: 150) jedhaatii barreessaa!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Duubatti", callback_data="back_main")]])
        )
    elif query.data == "withdraw":
        if balance < 100:
            await query.edit_message_text(
                f"🔴 WITHDRAW (Qarshii Baasuuf) 🟢\n\n❌ Qarshii baasuuf xiqqaan 100 Birr ta'uu qaba. Balance keessan {balance} Birr qofa.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Duubatti", callback_data="back_main")]])
            )
        else:
            await query.edit_message_text(
                f"🔴 WITHDRAW (Qarshii Baasuuf) 🟢\n\n⏩ Maqaa Bankii, Lakkoofsa Bankii fi Hamma qarshii baastan gadi kanaan bifa barreeffamaan nuuf barreessaa."
            )
    elif query.data == "play_menu":
        keyboard = [
            [InlineKeyboardButton("🎲 Tapha 5 Birr (Argannoo: 5-25)", callback_data="game_5")],
            [InlineKeyboardButton("🎲 Tapha 15 Birr (Argannoo: 15-75)", callback_data="game_15")],
            [InlineKeyboardButton("🎲 Tapha 25 Birr (Argannoo: 25-150)", callback_data="game_25")],
            [InlineKeyboardButton("🔙 Gara Main Menu", callback_data="back_main")]
        ]
        await query.edit_message_text("🎮 Taphawwan Carraa Filadhu:", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif query.data.startswith("game_"):
        cost = int(query.data.split("_")[1])
        if balance < cost:
            await query.edit_message_text(
                f"❌ Tapha kanaaf {cost} Birr si barbaachisa. Balance kee {balance} Birr dha. Maaloo dura Deposit godhi.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🟢 Deposit", callback_data="deposit")]])
            )
            return
        
        table_text = (
            f"🎮 TOUCH & WIN (Abbaa {cost} Birr)\n\n"
            "📋 GABATEE BADHAASAA / የሽልማት ሰንጠረዥ:\n"
            "Tapha 5   ->   5 - 25 Birr\n"
            "Tapha 15  ->  15 - 75 Birr\n"
            "Tapha 25  ->  25 - 150 Birr\n\n"
            "👉 Lakkoofsota 1 hanga 7 jiran keessaa lakkoofsa tokko tuquun badhaasa kee battalatti argadhu!\n\n"
            "🟢 Lakkoofsa kee filadhu:"
        )
        
        keyboard = []
        row = []
        for i in range(1, 8):
            row.append(InlineKeyboardButton(f"🔢 {i}", callback_data=f"play_{cost}_{i}"))
            if i % 3 == 0 or i == 7:
                keyboard.append(row)
                row = []
        keyboard.append([InlineKeyboardButton("🔙 Menu", callback_data="back_main")])
        
        await query.edit_message_text(table_text, reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif query.data.startswith("play_"):
        parts = query.data.split("_")
        cost = int(parts[1])
        user_choice = int(parts[2])
        
        current_bal = get_balance(user.id)
        if current_bal < cost:
            await query.edit_message_text("❌ Herregni kee gahaa miti. Maaloo kaffaltii gadii kanaan galchi.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🟢 Deposit", callback_data="deposit")]]))
            return
            
        update_balance(user.id, user.username, -cost)
        
        if cost == 5:
            win_amount = random.randint(5, 25)
        elif cost == 15:
            win_amount = random.randint(15, 75)
        else:
            win_amount = random.randint(25, 150)
            
        update_balance(user.id, user.username, win_amount)
        new_bal = get_balance(user.id)
        
        final_text = (
            f"🎮 BU'AA TAPHA TOUCH & WIN 🎮\n\n"
            f"👉 Lakkoofsa Ati Tuqte: 🔢 {user_choice}\n"
            f"🎁 🎉 BAGA GAMMADDE! 🎉 🎁\n\n"
            f"Lakkoofsa ati tuqte irratti badhaasni argame:\n"
            f"💰 +{win_amount} Birr\n\n"
            f"💳 Herrega keessan yeroo ammaa: {new_bal} Birr"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔄 Ammas Taphadhu", callback_data=f"game_{cost}")],
            [InlineKeyboardButton("🔙 Gara Main Menu", callback_data="back_main")]
        ]
        await query.edit_message_text(final_text, reply_markup=InlineKeyboardMarkup(keyboard))
            
    elif query.data == "back_main":
        await query.edit_message_text(f"🔴⚪⚫ Balance keessan: {balance} Birr\nFilannoo keessan gadii kanaan qoradhaa:", reply_markup=get_main_keyboard())

# ---- HANDLE DEPOSIT RECEIPT FROM USER ----
async def handle_deposit_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    photo_file = update.message.photo[-1].file_id
    caption_text = update.message.caption if update.message.caption else "Hamma qarshii hin barreeffamne"
    
    amount_detected = "".join([s for s in caption_text if s.isdigit()])
    final_amount = amount_detected if amount_detected else "0"

    keyboard = [
        [InlineKeyboardButton(f"✅ Mirkaneessi (+{final_amount} Birr)", callback_data=f"adm_dep_{final_amount}_{user.id}")],
        [InlineKeyboardButton("✅ 50 Birr", callback_data=f"adm_dep_50_{user.id}"), InlineKeyboardButton("✅ 100 Birr", callback_data=f"adm_dep_100_{user.id}")],
        [InlineKeyboardButton("✅ 200 Birr", callback_data=f"adm_dep_200_{user.id}"), InlineKeyboardButton("✅ 500 Birr", callback_data=f"adm_dep_500_{user.id}")],
        [InlineKeyboardButton("❌ Diduuf (Reject)", callback_data=f"adm_rej_0_{user.id}")]
    ]
    
    await context.bot.send_photo(
        chat_id=ADMIN_ID, 
        photo=photo_file, 
        caption=f"📩 Gaaffii Deposit Haaraa\n👤 Maamila: {user.first_name} (@{user.username})\n📝 Barreeffama isaan dhiisan: {caption_text}\nID: {user.id}", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    await update.message.reply_text("🚀 Ragaan keessan Admin-itti ergameera! Admin hanga mirkaneessutti maaloo obsaan eegaa.")

async def handle_text_requests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    text = update.message.text
    if user.id == ADMIN_ID: return
    
    keyboard = [
        [InlineKeyboardButton("✅ Baasii Mirkaneessi", callback_data=f"adm_wit_0_{user.id}")], 
        [InlineKeyboardButton("❌ Baasii Didu", callback_data=f"adm_rej_0_{user.id}")]
    ]
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 Withdraw Gaaffii:\n👤 Maamila: {user.first_name} (@{user.username})\n📝 Odeeffannoo Bankii: {text}\nID: {user.id}", reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text("🚀 Gaaffiin keessan Admin-itti ergameera. Admin keessan kaffalee yeroo xumuru ergaan siif dhufa.")

# ---- ADMIN VERIFICATION PROCESS ----
async def admin_verification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split("_")
    if len(parts) < 4 or parts[0] != "adm": return
    
    req_type = parts[1]      
    amount_str = parts[2]    
    user_id = int(parts[3])  
    
    try:
        amount = float(amount_str)
    except ValueError:
        amount = 0.0
    
    if req_type == "dep":
        if amount <= 0:
            await query.edit_message_text(text="❌ Dogoggora: Qarshii 0 galchuu hin dandeessu.")
            return
            
        update_balance(user_id, "", amount)
        new_bal = get_balance(user_id)
        msg_to_user = f"✅ Kaffaltiin keessan {amount} Birr mirkanaa'eera!\nHerrega keessan irratti dabalameera.\n💰 Balance ammaa: {new_bal} Birr"
        msg_to_admin = f"🟢 User {user_id} kaffaltii {amount} Birr mirkaneessitee jirta."
        
        try:
            await context.bot.send_message(chat_id=user_id, text=msg_to_user, reply_markup=get_main_keyboard())
        except Exception: pass
        
    elif req_type == "wit":
        msg_to_user = "✅ Gaaffiin qarshii baasuu keessan Admin biraa mirkanaa'eera!\nQarshii keessan bankii keessan irratti kaffalameera."
        msg_to_admin = f"🟢 User {user_id} Baasii isaa Mirkaneessitee jirta."
        try:
            await context.bot.send_message(chat_id=user_id, text=msg_to_user, reply_markup=get_main_keyboard())
        except Exception: pass
    else:
        msg_to_user = "❌ Dhiifama, gaaffiin keessan fudhatama hin arganne.\nRagaa kaffaltii keessan deebisaa mirkaneeffadha ykn Admin qunnamaa."
        msg_to_admin = f"🔴 User {user_id} gaaffii isaa diddee jirta."
        try:
            await context.bot.send_message(chat_id=user_id, text=msg_to_user, reply_markup=get_main_keyboard())
        except Exception: pass
        
    await query.edit_message_text(text=msg_to_admin)

def main():
    threading.Thread(target=run_health_server, daemon=True).start()
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click, pattern="^(deposit|withdraw|play_menu|check_balance|back_main|customer_service|game_.*|play_.*)$"))
    application.add_handler(CallbackQueryHandler(admin_verification, pattern="^adm_"))
    application.add_handler(MessageHandler(filters.PHOTO, handle_deposit_receipt))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_requests))
    
    application.run_polling()

if __name__ == "__main__": 
    main()
