import os
import dotenv
import pytest
from telethon import TelegramClient
from telethon.sessions import StringSession

# Remember to use your own values from my.telegram.org!
dotenv.read_dotenv()
# Your API ID, hash and session string here
api_id = int(os.environ["APP_ID"])
api_hash = os.environ["APP_HASH"]
session_str = os.environ["SESSION"]


@pytest.fixture
async def client() -> TelegramClient:
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
    await client.connect()
    
    yield client
    
    await client.disconnect()
    await client.disconnected