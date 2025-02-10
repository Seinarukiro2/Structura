from base64 import urlsafe_b64encode
from pytoniq_core import begin_cell

def get_comment_message(destination_address: str, amount: int, comment: str) -> dict:
    """Генерирует сообщение для TonConnect с комментарием."""
    
    payload = urlsafe_b64encode(
        begin_cell()
        .store_uint(0, 32)  # Op-code для комментария
        .store_string(comment)  # Сам комментарий (user_id)
        .end_cell()  # Завершаем ячейку
        .to_boc()  # Конвертируем в BOC
    ).decode()  # Переводим в Base64

    return {
        'address': destination_address,
        'amount': str(amount),
        'payload': payload
    }
