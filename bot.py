from datetime import datetime, timedelta
from telethon import TelegramClient, events, Button
from config.settings import API_ID, API_HASH, BOT_TOKEN, TON_WALLET_ADDRESS
from services.database import db
from prisma.types import DateTimeFilter
import hashlib
import os

# Создаем клиента Telethon
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def get_tonconnect_link(user_id, amount):
    amount_with_zero = int(float(amount) * 1e9)
    return f"ton://transfer/{TON_WALLET_ADDRESS}?amount={amount_with_zero}&text={user_id}"

def generate_unique_id():
    return hashlib.sha256(os.urandom(16)).hexdigest()[:12]

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    user_id = event.sender_id

    user = await db.user.find_first(where={"id": user_id})

    if user:
        await db.user.update(where={"id": user_id}, data={"state": "NAVIGATION"})
    else:
        await db.user.create(data={"state": "NAVIGATION", "id": user_id})

    
    text = (
        "Добро пожаловать в <b>STRUCTURA</b>, чтобы получить право на пропуск и стать 'sotrudnik, внесите пожалуйста ваши средства.\n\n"
        "// Мы не обещаем хорошее обращение с 'sotrudnik.\n\n"
    )

    buttons = [[Button.inline("Оплатить", 'pay')]]

    await bot.send_file(
        event.chat_id,
        "menu.jpg",
        caption=text,
        buttons=buttons,
        parse_mode="HTML"
    )

@bot.on(events.CallbackQuery(data='pay'))
async def pay_handler(event):
    user_id = event.sender_id

    # check if exists not expired payment
    payment = await db.payment.find_first(where={"userId": user_id, "status": "PENDING", "expiresAt": DateTimeFilter(gte=datetime.now())})

    if payment:
        await event.answer("У вас уже есть неоплаченный платеж")
        return

    await db.user.update(where={"id": user_id}, data={"state": "PAYMENT_PENDING"})

    amount = await db.setting.find_unique(where={"key": "payment_amount"})
    amount = float(f'{float(amount.value):.2f}')

    tonconnect_url = get_tonconnect_link(user_id, amount)

    comment = generate_unique_id()

    expiresAt = datetime.now() + timedelta(minutes=5)
    await db.payment.create(data={"userId": user_id, "amount": amount, "expiresAt": expiresAt, "uid": comment})

    text = (
        f"<b>Адрес для оплаты:</b> <code>{TON_WALLET_ADDRESS}</code>\n"
        f"<b>Мемо:</b> <code>{comment}</code>\n"
        f"<b>Сумма TON:</b> <code>{amount}</code>\n"
        f"<b>Оплата истекает через 5 минут</b>"
    )

    await bot.send_message(
        event.chat_id,
        text,
        buttons=[[Button.url("🔗 Открыть кошелек", tonconnect_url)]],
        parse_mode="HTML"
    )

print("Bot is running...")


async def main():
    await db.connect()

    # create a setting row with key "payment_amount" and value 40 if it doesn't exist
    await db.setting.upsert(
        where={
            "key": "payment_amount"
        },
        data={
            "create": {
                "key": "payment_amount",
                "value": "40"
            },
            "update": {}
        }
    )

    await bot.run_until_disconnected()


if __name__ == "__main__":
    bot.loop.run_until_complete(main())