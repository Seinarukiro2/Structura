from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_tonconnect_button(user_id: int) -> InlineKeyboardMarkup:
    """Создает кнопку TonConnect с id пользователя в параметрах."""
    tonconnect_url = f"https://app.tonkeeper.com/transfer/{TON_WALLET_ADDRESS}?amount=40000000000&text={user_id}"
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Оплатить 40 TON", url=tonconnect_url))
    return markup
