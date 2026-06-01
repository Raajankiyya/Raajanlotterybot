import asyncio
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# 1. Token fi Admin ID kee asitti galchi
API_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = "YOUR_ADMIN_ID_HERE"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

class WithdrawalForm(StatesGroup):
    phone = State()
    name = State()
    amount = State()

# --- Logic Tapha ---
def calculate_game_result(stake):
    lucky_numbers = [2, 5, 7]
    user_choice = random.randint(1, 7)
    if user_choice in lucky_numbers:
        if stake == 5: prize = random.randint(5, 25)
        elif stake == 15: prize = random.randint(15, 100)
        elif stake == 25: prize = random.randint(25, 150)
        else: prize = 0
        return True, user_choice, prize
    return False, user_choice, 0

# --- Keyboards ---
def get_main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Deposit / ማስገቢያ", callback_data="deposit_menu")],
        [InlineKeyboardButton(text="📤 Withdrawal / ማውጫ", callback_data="wd_phone")],
        [InlineKeyboardButton(text="🎮 Game Table / የጨዋታ ጠረጴዛ", callback_data="game_table")],
        [InlineKeyboardButton(text="🎧 Support / የደንበኞች አገልግሎት", callback_data="customer_service")]
    ])

def get_deposit_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔴 50", callback_data="dep_50"), InlineKeyboardButton(text="🟢 75", callback_data="dep_75")],
        [InlineKeyboardButton(text="🔴 100", callback_data="dep_100"), InlineKeyboardButton(text="🟢 150", callback_data="dep_150")],
        [InlineKeyboardButton(text="🔴 175", callback_data="dep_175"), InlineKeyboardButton(text="🟢 200", callback_data="dep_200")],
        [InlineKeyboardButton(text="🔴 250", callback_data="dep_250"), InlineKeyboardButton(text="🟢 500", callback_data="dep_500")],
        [InlineKeyboardButton(text="⬅️ Main Menu / ዋና ምናሌ", callback_data="main_menu")]
    ])

# --- Handlers ---
@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Baga nagaan dhuftan! / እንኳን ደህና መጡ!", reply_markup=get_main_kb())

@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    await callback.message.edit_text("Main Menu / ዋና ምናሌ:", reply_markup=get_main_kb())

@router.callback_query(F.data == "deposit_menu")
async def deposit_menu(callback: CallbackQuery):
    await callback.message.edit_text("Gatii filadhaa / ዋጋ ይምረጡ:", reply_markup=get_deposit_kb())

# Logic Deposit fi Admin Confirmation
@router.callback_query(F.data.startswith("dep_"))
async def deposit_handler(callback: CallbackQuery):
    amount = callback.data.split("_")[1]
    user = callback.from_user
    
    admin_msg = (f"🔔 Deposit Haaraa!\n\n"
                 f"👤 User: {user.full_name} (@{user.username})\n"
                 f"💰 Amount: {amount} ETB\n"
                 f"📅 Yeroo: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ Mirkaneessi ({amount})", callback_data=f"conf_{amount}_{user.id}")],
        [InlineKeyboardButton(text="❌ Diduuf", callback_data=f"reject_{user.id}")]
    ])
    
    await bot.send_message(chat_id=ADMIN_ID, text=admin_msg, reply_markup=kb)
    await callback.message.answer("🚀 Ragaan keessan Admin-itti ergameera!")

@router.callback_query(F.data.startswith("conf_"))
async def admin_confirm(callback: CallbackQuery):
    _, amount, user_id = callback.data.split("_")
    await bot.send_message(chat_id=user_id, text=f"✅ Deposit keessan {amount} ETB mirkanaa'eera!")
    await callback.message.edit_text(f"✅ Mirkaneeffameera ({amount} ETB).")

@router.callback_query(F.data.startswith("reject_"))
async def admin_reject(callback: CallbackQuery):
    user_id = callback.data.split("_")[1]
    await bot.send_message(chat_id=user_id, text="❌ Deposit keessan hin milkoofne.")
    await callback.message.edit_text("❌ Didameera.")

# Withdrawal fi Game Handlers
@router.callback_query(F.data == "wd_phone")
async def wd_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Lakk. bilbilaa kee galchi / ስልክ ቁጥርዎን ያስገቡ:")
    await state.set_state(WithdrawalForm.phone)

# ... (Logic kan biraa asitti itti fufa)

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())        [InlineKeyboardButton(text="📤 Withdrawal / ማውጫ", callback_data="wd_phone")],
        [InlineKeyboardButton(text="🎮 Game Table / የጨዋታ ጠረጴዛ", callback_data="game_table")],
        [InlineKeyboardButton(text="🎧 Support / የደንበኞች አገልግሎት", callback_data="customer_service")]
    ])

def get_deposit_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔴 50", callback_data="dep_50"), InlineKeyboardButton(text="🟢 75", callback_data="dep_75")],
        [InlineKeyboardButton(text="🔴 100", callback_data="dep_100"), InlineKeyboardButton(text="🟢 150", callback_data="dep_150")],
        [InlineKeyboardButton(text="🔴 175", callback_data="dep_175"), InlineKeyboardButton(text="🟢 200", callback_data="dep_200")],
        [InlineKeyboardButton(text="🔴 250", callback_data="dep_250"), InlineKeyboardButton(text="🟢 500", callback_data="dep_500")],
        [InlineKeyboardButton(text="⬅️ Main Menu / ዋና ምናሌ", callback_data="main_menu")]
    ])

def get_game_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="5 ETB", callback_data="play_5"), InlineKeyboardButton(text="15 ETB", callback_data="play_15"), InlineKeyboardButton(text="25 ETB", callback_data="play_25")],
        [InlineKeyboardButton(text="⬅️ Main Menu / ዋና ምናሌ", callback_data="main_menu")]
    ])

# --- Handlers ---
@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Baga nagaan dhuftan! / እንኳን ደህና መጡ!", reply_markup=get_main_kb())

@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    await callback.message.edit_text("Main Menu / ዋና ምናሌ:", reply_markup=get_main_kb())

@router.callback_query(F.data == "game_table")
async def game_table(callback: CallbackQuery):
    await callback.message.edit_text("🎮 Tapha filadhaa / ጨዋታ ይምረጡ:", reply_markup=get_game_kb())

@router.callback_query(F.data.startswith("play_"))
async def play_game(callback: CallbackQuery):
    stake = int(callback.data.split("_")[1])
    won, number, prize = calculate_game_result(stake)
    msg = f"Lakkoofsa: {number}\n" + ("🎉 Injifatteetta! / አሸንፈዋል! " + str(prize) + " ETB" if won else "❌ Hin injifanne. / አልተሳካም.")
    await callback.message.answer(msg, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Next Game / ቀጣይ ጨዋታ", callback_data="game_table")]
    ]))

@router.callback_query(F.data == "customer_service")
async def customer_service(callback: CallbackQuery):
    await callback.message.answer("📞 Gargaarsaaf: @admin_username")

@router.callback_query(F.data == "wd_phone")
async def wd_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Lakk. bilbilaa kee galchi / ስልክ ቁጥርዎን ያስገቡ:")
    await state.set_state(WithdrawalForm.phone)

@router.message(WithdrawalForm.phone)
async def wd_name(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Maqaa kee galchi / ስምዎን ያስገቡ:")
    await state.set_state(WithdrawalForm.name)

@router.message(WithdrawalForm.name)
async def wd_amount(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Gatii baasuu barbaaddu galchi / ማውጣት የሚፈልጉትን መጠን ያስገቡ:")
    await state.set_state(WithdrawalForm.amount)

@router.message(WithdrawalForm.amount)
async def wd_finish(message: Message, state: FSMContext):
    data = await state.update_data(amount=message.text)
    await message.answer(f"✅ Odeeffannoon kee qabameera!\n\n📱 Bilbila: {data['phone']}\n👤 Maqaa: {data['name']}\n💰 Gatii: {data['amount']}")
    await state.clear()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
