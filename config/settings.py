import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
TON_WALLET_ADDRESS = os.getenv("TON_WALLET_ADDRESS")
TON_API_KEY = os.getenv("TON_API_KEY")
PRIVATE_CHAT_LINK = os.getenv("PRIVATE_CHAT_LINK")
