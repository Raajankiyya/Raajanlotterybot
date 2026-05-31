import os
import random
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Token, Admin ID fi Telebirr kee
TOKEN = "8200095818:AAHGl2VtiKQbt3dA6Vg5UOVB4H0g7QyVUOI"
ADMIN_ID = 6271558160
TELEBIRR_NUMBER = "0924720606"

# ---- DATABASE QOPHEESSUU ----
def init_db():
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0.0
        )
    """)
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return 0.0

def update_balance(user_id, username, amount):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, balance) VALUES (?, ?, 0.0)", (user_id, username))
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

# Database jalqabsiisuu
init_db()

# ---- BOT ACTIONS ----

# Simannaa gubbaa (Start)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    balance = get_balance(user.id)
    
    # Button-oota dizaayinii halluu ati barbaaddeen (Emojii Magariisa, Cuquliisa, fi Diimaan xaxamee)
    keyboard = [
        [
            InlineKeyboardButton("🟢 DEPOSIT (Galchuuf) 🟢", callback_data="deposit"),
            InlineKeyboardButton("🔴 WITHDRAW (Baasuuf) 🟢", callback_data="withdraw")
        ],
        [
            InlineKeyboardButton("🎮 Tapha Jalqabi (Play Game) 🎲", callback_data="play_menu")
        ],
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

# Inline Buttons Actions
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
            f"💳 **Herrega Kee / ሂሳብዎ:**\n\n"
            f"Afaan Oromoo: Balance keessan yeroo ammaa `{balance} Birr` dha.\n"
            f"አማርኛ: የአሁኑ ሂሳብዎ `{balance} Birr` ነው።",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Gara Fuladuraatti", callback_data="back_main")]])
        )
        
    elif query.data == "deposit":
        await query.edit_message_text(
            f"🟢 **DEPOSIT (Qarshii Galchuuf) 🟢**\n\n"
            f"1. Lakkoofsa **Telebirr** keenya: `{TELEBIRR_NUMBER}` irratti kaffalaa.\n"
            f"2. Fakkii (Screenshot) kaffaltii bot kanaaf ergaa.\n\n"
            f"Hamma barbaaddan deposit gochuu ni dandeessu! / የፈለጉትን ያህል ማስገባት ይችላሉ!"
        )
        
    elif query.data == "withdraw":
        if balance < 100:
            await query.edit_message_text(
                f"🔴 **WITHDRAW (Qarshii Baasuuf) 🟢**\n\n"
                f"❌ **Dhiifama / ይቅርታ!**\n\n"
                f"Afaan Oromoo: Qarshii baasuuf xiqqaan **100 Birr** ta'uu qaba. Balance keessan `{balance} Birr` qofa.\n"
                f"አማርኛ: ማውጣት የሚቻለው አነስተኛው መጠን **100 Birr** ነው። የእርስዎ ሂሳብ `{balance} Birr` ነው።",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Duubatti", callback_data="back_main")]])
            )
        else:
            await query.edit_message_text(
                f"🔴 **WITHDRAW (Qarshii Baasuuf) 🟢**\n\n"
                f"⏩ Maqaa Bankii, Lakkoofsa fi Hamma qarshii baastan (Minimum 100) nuuf barreessaa.\n"
                f"ምሳሌ: `Telebirr, 09xxxxxxxx, 150 Birr`"
            )
            
    elif query.data == "play_menu":
        keyboard = [
            [InlineKeyboardButton("🎲 Tapha 5 Birr (Carraa 5-25)", callback_data="game_5")],
            [InlineKeyboardButton("🎲 Tapha 15 Birr (Carraa 15-75)", callback_data="game_15")],
            [InlineKeyboardButton("🎲 Tapha 25 Birr (Carraa 25-150)", callback_data="game_25")],
            [InlineKeyboardButton("🔙 Gara Fuladuraatti", callback_data="back_main")]
        ]
        await query.edit_message_text("🎮 **Taphawwan Carraa Filadhu / የዕድል ጨዋታ ይምረጡ:**", reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif query.data.startswith("game_"):
        cost = int(query.data.split("_")[1])
        if balance < cost:
            await query.edit_message_text(
                f"❌ **Qarshii Gahaa Hin Qabdu / በቂ ሂሳብ የለዎትም!**\n\n"
                f"Tapha kanaaf {cost} Birr si barbaachisa. Balance kee `{balance} Birr` dha. Maaloo dura Deposit godhi.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🟢 Deposit", callback_data="deposit")]])
            )
            return
            
        update_balance(user.id, user.username, -cost)
        nums = [random.randint(1, 7) for _ in range(3)]
        
        if cost == 5:
            win_amount = random.randint(5, 25)
        elif cost == 15:
            win_amount = random.randint(15, 75)
        else:
            win_amount = random.randint(25, 150)
            
        update_balance(user.id, user.username, win_amount)
        new_bal = get_balance(user.id)
        
        result_text = (
            f"🎲 **Bu'aa Carraa Kee / የዕድልዎ ውጤት:**\n\n"
            f"🔢 Lakkoofsota Keessan: **{nums[0]} - {nums[1]} - {nums[2]}**\n"
            f"🎁 Badhaasa keessan: **+{win_amount} Birr** 🎉\n\n"
            f"💳 Balance ammaa: `{new_bal} Birr`"
        )
        keyboard = [[InlineKeyboardButton("🔄 Ammas Taphadhu", callback_data=f"game_{cost}")], [InlineKeyboardButton("🔙 Menu", callback_data="back_main")]]
        await query.edit_message_text(result_text, reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif query.data == "back_main":
        keyboard = [
            [
                InlineKeyboardButton("🟢 DEPOSIT (Galchuuf) 🟢", callback_data="deposit"),
                InlineKeyboardButton("🔴 WITHDRAW (Baasuuf) 🟢", callback_data="withdraw")
            ],
            [
                InlineKeyboardButton("🎮 Tapha Jalqabi (Play Game) 🎲", callback_data="play_menu")
            ],
            [
                InlineKeyboardButton("🔵 CUSTOMER SERVICE 🟢", callback_data="customer_service"),
                InlineKeyboardButton("💳 Balance (Herrega Kee)", callback_data="check_balance")
            ]
        ]
        await query.edit_message_text(f"🔴⚪⚫ Gara fuula duraatti deebitaniittu.\nBalance: {balance} Birr", reply_markup=InlineKeyboardMarkup(keyboard))

# Deposit Receipt 
async def handle_deposit_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    photo_file = update.message.photo[-1].file_id
    keyboard = [[InlineKeyboardButton("✅ Mirkaneessi (Approve)", callback_data=f"app_dep_{user.id}")], [InlineKeyboardButton("❌ Diduuf (Reject)", callback_data=f"rej_dep_{user.id}")]]
    
    await context.bot.send_photo(
        chat_id=ADMIN_ID, photo=photo_file,
        caption=f"📩 **Deposit Haaraan Dhufeera!**\n👤 Maamila: {user.first_name} (@{user.username})\n🆔 User ID: {user.id}\n\nManual-iin ilaaliiti herrega isaa oliif dabali.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    await update.message.reply_text("🚀 Ragaan keessan Admin-itti ergameera. To'atamee hamma mirkanaa'utti gadi nu eegaa!")

# Withdraw Request
async def handle_text_requests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    text = update.message.text
    if user.id == ADMIN_ID: return

    keyboard = [[InlineKeyboardButton("✅ Baasii Mirkaneessi", callback_data=f"app_wit_{user.id}")], [InlineKeyboardButton("❌ Baasii Didu", callback_data=f"rej_wit_{user.id}")]]
    
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 **Gaaffiin Qarshii Baasuu (Withdraw) Dhufeera!**\n👤 Maamila: {user.first_name}\n🆔 User ID: {user.id}\n📝 Odeeffannoo: {text}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    await update.message.reply_text("🚀 Gaaffiin keessan Admin-itti ergameera. Nuuf obsaa!")

# Admin Verification Buttons
async def admin_verification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    action, req_type, user_id = data.split("_")
    user_id = int(user_id)
    
    if action == "app":
        if req_type == "dep":
            update_balance(user_id, "", 100) 
            msg_to_user = "✅ Kaffaltiin keessan mirkanaa'eera! Balance keessan irratti dabalameera!"
        else:
            update_balance(user_id, "", -100)
            msg_to_user = "✅ Gaaffiin qarshii baasuu keessan fudhatama argatee isiniif ergameera!"
        msg_to_admin = f"🟢 User ID {user_id} Mirkaneessitee jirta."
    else:
        msg_to_user = "❌ Dhiifama, gaaffiin keessan fudhatama hin arganne."
        msg_to_admin = f"🔴 User ID {user_id} Diddee jirta."
        
    try:
        await context.bot.send_message(chat_id=user_id, text=msg_to_user)
        await query.edit_message_caption(caption=f"{query.message.caption}\n\n{msg_to_admin}") if query.message.photo else await query.edit_message_text(text=f"{query.message.text}\n\n{msg_to_admin}")
    except Exception:
        pass

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click, pattern="^(deposit|withdraw|play_menu|check_balance|back_main|customer_service|game_.*)$"))
    application.add_handler(CallbackQueryHandler(admin_verification, pattern="^(app|rej)_"))
    application.add_handler(MessageHandler(filters.PHOTO, handle_deposit_receipt))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_requests))
    application.run_polling()

if __name__ == "__main__": main()
