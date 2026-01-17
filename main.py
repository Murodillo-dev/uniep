import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import BOT_TOKEN, ADMINS

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# mapping: admin xabar id → (user_id, user_message_id)
admin_to_user_mapping = {}


# ---------------- /start ----------------
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Ushbu bot orqali yuborilgan savol va takliflar Ta’lim sifatini nazorat qilish bo‘limi boshlig‘i tomonidan belgilangan tartibda ko‘rib chiqilib, javob taqdim etiladi."
    )


# ---------------- Handle Messages ----------------
@dp.message()
async def handle_messages(message: Message):
    user_id = message.from_user.id

    # ======= ADMIN yozayotgan bo‘lsa =======
    if user_id in ADMINS:

        if not message.reply_to_message:
            await message.reply("Iltimos, javobni faqat reply orqali yozing.")
            return

        reply_msg = message.reply_to_message

        if reply_msg.message_id not in admin_to_user_mapping:
            await message.reply("Xabar formatini topa olmadim.")
            return

        target_user_id, user_message_id = admin_to_user_mapping[reply_msg.message_id]

        try:
            await bot.send_message(
                chat_id=target_user_id,
                text=f"Admin javobi:\n{message.text}",
                reply_to_message_id=user_message_id
            )
        except Exception as e:
            await message.reply(f"Xabar yuborilmadi: {e}")
        return

    # ======= USER yozayotgan bo‘lsa =======
    user_text = message.text or "<media>"

    username = message.from_user.username or "No username"
    full_name = message.from_user.full_name or "No name"

    for admin_id in ADMINS:
        try:
            sent_message = await bot.send_message(
                chat_id=admin_id,
                text=(
                    f"Yangi xabar:\n{user_text}\n\n"
                    # f"User ID: {user_id}\n"
                    f"Foylanuvchi nomi: @{username}\n"
                    f"Foydalanuvchining To'liq ismi : {full_name}"
                )
            )

            # mapping: admin_message_id → (user_id, user_message_id)
            admin_to_user_mapping[sent_message.message_id] = (
                user_id,
                message.message_id
            )

        except Exception as e:
            print(f"Xabar adminga yuborilmadi: {e}")

    await message.answer("Xabaringiz adminlarga yuborildi tez orada javob beramiz ✅")


# ---------------- MAIN ----------------

# ---------------- Handle Messages ---------------

async def main():
    print("Bot ishga tushdi va doimiy ishlayapti...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

