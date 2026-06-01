import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

# Token fi Admin ID kee asitti galchi
API_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = "YOUR_ADMIN_ID_HERE"

# Logging setup - rakkoo Render irratti argachuuf gargaara
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

# 1. Deposit Panel (Bifa table 50, 100, 150, 200, 500)
def get_deposit_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="50", callback_data="dep_50"), InlineKeyboardButton(text="100", callback_data="dep_100")],
        [InlineKeyboardButton(text="150", callback_data="dep_150"), InlineKeyboardButton(text="200", callback_data="dep_200")],
        [InlineKeyboardButton(text="500", callback_data="dep_500")]
    ])

@router.message(Command("start"))
async def start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Deposit (Qarshii Galchuuf)", callback_data="deposit_menu")]
    ])
    await message.answer("Baga nagaan dhuftan! Maaloo filannoo filadhaa:", reply_markup=kb)

@router.callback_query(F.data == "deposit_menu")
async def deposit_menu(callback: CallbackQuery):
    await callback.message.edit_text("🟢 **DEPOSIT (Qarshii Galchuuf)** 🟢\n\nGatii filadhaa:", reply_markup=get_deposit_kb(), parse_mode="Markdown")

# 2. Qajeelfama Telebirr (Screenshot_20260601_102058_Telegram X.jpg)
@router.callback_query(F.data.startswith("dep_"))
async def show_payment_info(callback: CallbackQuery):
    amount = callback.data.split("_")[1]
    
    payment_info = (
        "🟢 **DEPOSIT (Qarshii Galchuuf)** 🟢\n\n"
        f"Gatii filatte: {amount} ETB\n\n"
        "1. Lakkoofsa **Telebirr** keenya: `0924720606` irratti kaffalaa.\n"
        "2. Fakkii (Screenshot) kaffaltii bot kanaaf ergaa."
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ergeera (Screenshot)", callback_data=f"confirm_{amount}")]
    ])
    
    await callback.message.edit_text(payment_info, reply_markup=kb, parse_mode="Markdown")

# 3. Mirkaneessuu
@router.callback_query(F.data.startswith("confirm_"))
async def confirm_payment(callback: CallbackQuery):
    await callback.answer("Ergaa keessan hordofaa jirra!")

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
