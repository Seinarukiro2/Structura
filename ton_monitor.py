import asyncio
import logging
import time
import telebot
from datetime import datetime, timedelta
from pytoniq import LiteBalancer, Address as AddressIq
from pytoncenter import get_client
from pytoncenter.v3.models import *
from config.settings import BOT_TOKEN, TON_WALLET_ADDRESS, PRIVATE_CHAT_ID, TON_API_KEY, PAYMENT_STEP
from services.database import db

# Логирование
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем telebot (только для отправки сообщений)
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Подключаем провайдера TON
provider = LiteBalancer.from_mainnet_config(1)
provider._logger.setLevel(logging.ERROR)

async def check_transactions():
    """Проверяет новые транзакции и отправляет уведомление пользователю через telebot."""
    await db.connect()

    client = get_client(
        version="v3",
        network="mainnet",
        api_key=TON_API_KEY,
    )

    await provider.start_up()

    async for tx in client.subscribe_tx(
        SubscribeTransactionRequest(
            account=TON_WALLET_ADDRESS,
            start_time=time.time() - 3600 * 3,
            limit=30,
            interval=5,
        )
    ):
        # try:
        # payments_pending = await db.payment.find_many(where={"status": "PENDING", "expiresAt": DateTimeFilter(
        #     gte=datetime.now() - timedelta(minutes=5)
        # )})

        # print(payments_pending)

        sender = AddressIq(tx.in_msg.source).to_str(1, 1, 1)
        value_ton = float(tx.in_msg.value or 0) / 1e9

        comment = ""

        if tx.in_msg.message_content.decoded is not None:
            if isinstance(tx.in_msg.message_content.decoded, TextComment):
                comment = tx.in_msg.message_content.decoded.comment
            else:
                comment = tx.in_msg.message_content.decoded.hex_comment

        if comment != "":
            payment = await db.payment.find_unique(where={"uid": comment, "status": "PENDING"})

            if payment and payment.expiresAt > datetime.now(tz=payment.expiresAt.tzinfo):
                MIN_PAYMENT_AMOUNT = payment.amount
                if value_ton >= MIN_PAYMENT_AMOUNT:
                    print(f"Транзакция: {sender} -> {TON_WALLET_ADDRESS} {value_ton} TON, Комментарий: {comment}")
                    user_id = payment.userId

                    invite_data = bot.create_chat_invite_link(PRIVATE_CHAT_ID, expire_date=datetime.now() + timedelta(days=1), member_limit=1)
                    PRIVATE_CHAT_LINK = invite_data.invite_link

                    bot.send_message(user_id, f"✅ Ваш платеж на {value_ton} TON получен!\n🎉 {PRIVATE_CHAT_LINK}", parse_mode="HTML", disable_web_page_preview=True)

                    setting_payment_amount = await db.setting.find_unique(where={"key": "payment_amount"})

                    await db.payment.update(where={"id": payment.id}, data={"status": "SUCCESS"})
                    await db.user.update(where={"id": user_id}, data={"state": "PAYMENT_SUCCESS", "wallet": sender})
                    await db.setting.update(where={"key": "payment_amount"}, data={"value": str(float(setting_payment_amount.value) + float(PAYMENT_STEP))})
        # except Exception as e:
        #     print(e)
        #     logger.error(f"Ошибка при обработке транзакции: {e}")

if __name__ == "__main__":
    asyncio.run(check_transactions())
