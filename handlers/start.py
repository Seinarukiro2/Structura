from aiogram import types, Dispatcher
from config.settings import PRIVATE_CHAT_LINK
from utils.keyboard import get_tonconnect_button

async def start_command(message: types.Message):
    """Обработчик команды /start, отправляет кнопку TonConnect."""
    text = (
        "Привет! Для доступа к закрытому чату необходимо оплатить 40 TON.\n"
        "Нажмите кнопку ниже, чтобы произвести оплату:"
    )
    await message.answer(text, reply_markup=get_tonconnect_button(message.from_user.id))

def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
