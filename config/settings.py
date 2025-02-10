import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TON_WALLET_ADDRESS = os.getenv("TON_WALLET_ADDRESS")
TON_API_KEY = os.getenv("TON_API_KEY")
TON_API_URL = "https://tonapi.io"
PRIVATE_CHAT_LINK = os.getenv("PRIVATE_CHAT_LINK")
MIN_PAYMENT_AMOUNT = 40.0
