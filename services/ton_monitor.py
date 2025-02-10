import asyncio
import logging
import time
import telebot
from pytoniq import LiteBalancer, Address as AddressIq
from pytoniq.tlb import Cell
from config.settings import BOT_TOKEN, TON_WALLET_ADDRESS, MIN_PAYMENT_AMOUNT, PRIVATE_CHAT_LINK

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем telebot (только для отправки сообщений)
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Подключаем провайдера TON
provider = LiteBalancer.from_mainnet_config(1)

async def check_transactions():
    """Проверяет новые транзакции и отправляет уведомление пользователю через telebot."""
    await provider.start_up()

    while True:
        try:
            async for tx in provider.subscribe_transactions(TON_WALLET_ADDRESS, limit=10):
                sender = AddressIq(tx.in_msg.source).to_str(1, 1, 1)
                value_ton = float(tx.in_msg.value or 0) / 1e9

                try:
                    if tx.in_msg.message_content.body:
                        body_cell = Cell.from_boc(tx.in_msg.message_content.body)[0]
                        cs = body_cell.begin_parse()
                        if cs.bits >= 32:
                            cs.load_uint(32)  # Пропускаем op-code
                            comment = cs.load_snake_string()
                        else:
                            comment = ""
                    else:
                        comment = ""
                except Exception:
                    comment = ""

                logger.info(f"Транзакция: {sender} -> {TON_WALLET_ADDRESS} {value_ton} TON, Комментарий: {comment}")

                if value_ton >= MIN_PAYMENT_AMOUNT and comment.isdigit():
                    user_id = int(comment)
                    bot.send_message(user_id, f"✅ Ваш платеж на {value_ton} TON получен!\n🎉 {PRIVATE_CHAT_LINK}")

        except Exception as e:
            logger.error(f"Ошибка при проверке транзакций: {e}")

        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(check_transactions())
