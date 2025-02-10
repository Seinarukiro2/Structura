import asyncio
from telethon import TelegramClient, events, Button
from config.settings import API_ID, API_HASH, BOT_TOKEN, TON_WALLET_ADDRESS

# Создаем клиента Telethon
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def get_tonconnect_link(user_id, amount):
    amount_with_zero = amount * 1000000000
    return f"ton://transfer/{TON_WALLET_ADDRESS}?amount={amount_with_zero}&text={user_id}"

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    user_id = event.sender_id
    amount = 40
    tonconnect_url = get_tonconnect_link(user_id, amount)

    text = (
        "Добро пожаловать в <b>STRUCTURA</b>, чтобы получить право на пропуск и стать 'sotrudnik, внесите пожалуйста ваши средства.\n\n"
        "// Мы не обещаем хорошее обращение с 'sotrudnik.\n\n"
        f"<b>Адрес для оплаты:</b> <code>{TON_WALLET_ADDRESS}</code>\n"
        f"<b>Мемо:</b> <code>{user_id}</code>\n"
        f"<b>Сумма TON:</b> <code>...</code>"
    )

    buttons = [[Button.url("🔗 Оплатить", tonconnect_url)]]

    await bot.send_file(
        event.chat_id,
        "menu.jpg",
        caption=text,
        buttons=buttons,
        parse_mode="HTML"
    )

print("Бот запущен и готов к работе!")
bot.run_until_disconnected()