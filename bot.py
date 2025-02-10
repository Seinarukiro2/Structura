import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from config.settings import BOT_TOKEN
from handlers.start import register_handlers_start
from services.ton_monitor import check_transactions

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

async def main():
    register_handlers_start(dp)
    
    loop = asyncio.get_event_loop()
    loop.create_task(check_transactions())

    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
