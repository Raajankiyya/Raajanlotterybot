import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Token, Admin ID fi Telebirr kee sirriitti asitti galeera
TOKEN = "8200095818:AAHGl2VtiKQbt3dA6Vg5UOVB4H0g7QyVUOI"
ADMIN_ID = 6271558160  # ID Telegram kee
TELEBIRR_NUMBER = "0924720606"  # Lakkoofsa Telebirr kee

# Maamila jalqaba simachuu (Welcome Message - Afaan Lamaan & Flag)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("💰 Qarshii Galchuuf (Deposit)", callback_data="deposit"),
            InlineKeyboardButton("💸 Qarshii Baasuuf (Withdraw)", callback_data="withdraw")
        ],
        [
            InlineKeyboardButton("💰 ብር ለማስገባት (Deposit)", callback_data="deposit_am"),
            InlineKeyboardButton("💸 ብር ለማውጣት (Withdraw)", callback_data="withdraw_am")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🔴🔴🔴🔴🔴🔴🔴🔴\n"
        "⚪⚪⚪🌳⚪⚪⚪\n"
        "⚫⚫⚫⚫⚫⚫⚫⚫\n\n"
        "**[Afaan Oromoo]**\n"
        "Baga Nagaan Dhuftan! Gara Bot kaffaltii keenyaatti. Maaloo filannoo keessan tuqaa.\n\n"
        "**[አማርኛ]**\n"
        "እንኳን በደህና መጡ! ወደ ክፍያ ቦታችን። እባክዎ ምርጫዎን ይጫኑ።"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# Filannoo Button-ii addaan baasuu
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # ---- AFAAN OROMOO ----
    if query.data == "deposit":
        await query.edit_message_text(
            f"⏩ **Kaffaltii Raawwachuuf:**\n\n"
            f"1. Lakkoofsa **Telebirr** keenya: `{TELEBIRR_NUMBER}` irratti qarshii ergaa.\n"
            f"2. Erga argattanii booda **Ragaa kaffaltii (Screen-shot/Photo)** Bot kanaaf ergaa.\n\n"
            f"Nuyi ilaallee yoo mirkaneessinu (verify) isiniif gadi lakkifama.",
            parse_mode="Markdown"
        )
    elif query.data == "withdraw":
        await query.edit_message_text(
            "⏩ **Qarshii Baasuuf:**\n\n"
            "Maaloo gadi kanaan: *Maqaa Bankii/Telebirr, Lakkoofsa Herregaa fi Hamma qarshii* baasuu barbaaddan nuuf barreessaa.\n"
            "Fakkeenya: `Telebirr, 09xxxxxxxx, 500 Birr`",
            parse_mode="Markdown"
        )
        
    # ---- AMHARIC ----
    elif query.data == "deposit_am":
        await query.edit_message_text(
            f"⏩ **ክፍያ ለመፈጸም:**\n\n"
            f"1. በኛ **Telebirr** ቁጥር: `{TELEBIRR_NUMBER}` ላይ ብሩን ይላኩ።\n"
            f"2. ከላኩ በኋላ **የክፍያ ማረጋገጫ (Screen-shot/ፎቶ)** ለዚህ ቦት ይላኩ።\n\n"
            f"እኛ አይተን ስናረጋግጥ (verify) ይለቀቅልዎታል።",
            parse_mode="Markdown"
        )
    elif query.data == "withdraw_am":
        await query.edit_message_text(
            "⏩ **ብር ለማውጣት:**\n\n"
            "እባክዎ ከታች ባለው መልኩ: *የባንክ/ቴሌብር ስም፣ የሂሳብ ቁጥር እና ማውጣት የሚፈልጉትን የብር መጠን* ይጻፉልን።\n"
            "ምሳሌ: `Telebirr, 09xxxxxxxx, 500 Birr`",
            parse_mode="Markdown"
        )

# Yeroo maamilli ragaa kaffaltii (Fakkii) ergu gara Adminitti dabarsuu
async def handle_deposit_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    photo_file = update.message.photo[-1].file_id
    
    keyboard = [
        [InlineKeyboardButton("✅ Mirkaneessi (Approve)", callback_data=f"app_dep_{user.id}")],
        [InlineKeyboardButton("❌ Diduuf (Reject)", callback_data=f"rej_dep_{user.id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo_file,
        caption=f"📩 **Ragaan Kaffaltii (Deposit) Haaraan Dhufeera!**\n\n"
                f"👤 Maamila: {user.first_name} (@{user.username})\n"
                f"🆔 User ID: {user.id}\n\n"
                f"Maaloo kaffaltii kana manual-iin ilaaliiti mirkaneessi.",
        reply_markup=reply_markup
    )
    await update.message.reply_text("🚀 Ragaan keessan Admin-itti ergameera. To'atamee hamma mirkanaa'utti gadi nu eegaa! / ማረጋገጫዎ ለባለቤቱ ተልኳል። እስከሚረጋገጥ ድረስ በትዕግስት ይጠብቁ!")

# Yeroo maamilli ergaa barreeffamaa ergu gara Adminitti dabarsuu
async def handle_text_requests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    text = update.message.text
    
    if user.id == ADMIN_ID:
        return

    keyboard = [
        [InlineKeyboardButton("✅ Baasii Mirkaneessi", callback_data=f"app_wit_{user.id}")],
        [InlineKeyboardButton("❌ Baasii Didu", callback_data=f"rej_wit_{user.id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 **Gaaffiin Qarshii Baasuu (Withdraw) Dhufeera!**\n\n"
             f"👤 Maamila: {user.first_name} (@{user.username})\n"
             f"🆔 User ID: {user.id}\n"
             f"📝 Odeeffannoo: {text}\n\n"
             f"Erga herrega isaaniitti ergitee booda Approve godhi.",
        reply_markup=reply_markup
    )
    await update.message.reply_text("🚀 Gaaffiin keessan Admin-itti ergameera. Nuuf obsaa! / ጥያቄዎ ለባለቤቱ ተልኳል። እናመሰግናለን!")

# Admin yeroo Button Approve/Reject tuqu maamilaaf deebii erguu
async def admin_verification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    data = query.data
    action, req_type, user_id = data.split("_")
    user_id = int(user_id)
    
    if action == "app":
        msg_to_user = (
            "✅ Kaffaltiin ykn gaaffiin qarshii baasuu keessan Adminiin ilaalamee mirkanaa'eera! Galatoomaa.\n"
            "✅ የክፍያ ወይም የብር ማውጣት ጥያቄዎ በባለቤቱ ታይቶ ጸድቋል! እናመሰግናለን።"
        )
        msg_to_admin = f"🟢 User ID {user_id} Mirkaneessitee jirta."
    else:
        msg_to_user = (
            "❌ Dhiifama, gaaffiin keessan Adminiin ilaalamee fudhatama hin arganne. Maaloo odeeffannoo sirrii ergaa.\n"
            "❌ ይቅርታ፣ ጥያቄዎ በባለቤቱ ተቀባይነት አላገኘም። እባክዎ ትክክለኛ መረጃ ይላኩ።"
        )
        msg_to_admin = f"🔴 User ID {user_id} Diddee (Reject) jirta."
        
    try:
        await context.bot.send_message(chat_id=user_id, text=msg_to_user)
        if query.message.photo:
            await query.edit_message_caption(caption=f"{query.message.caption}\n\n{msg_to_admin}")
        else:
            await query.edit_message_text(text=f"{query.message.text}\n\n{msg_to_admin}")
    except Exception as e:
        if query.message.photo:
            await query.edit_message_caption(caption=f"{query.message.caption}\n\n❌ Dogoggora: {e}")
        else:
            await query.edit_message_text(text=f"{query.message.text}\n\n❌ Dogoggora: {e}")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click, pattern="^(deposit|withdraw|deposit_am|withdraw_am)$"))
    application.add_handler(CallbackQueryHandler(admin_verification, pattern="^(app|rej)_"))
    application.add_handler(MessageHandler(filters.PHOTO, handle_deposit_receipt))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_requests))
    
    print("Bot-iin manual verification hojii jalqabeera...")
    application.run_polling()

if __name__ == "__main__":
    main()
