import os
import pytest
from telethon import TelegramClient
from telethon.sessions import StringSession
from common_parts import (
    get_reply_of_message_of_id,
)

# Your API ID, hash and session string here
api_id = int(os.environ["APP_ID"])
api_hash = os.environ["APP_HASH"]
session_str = os.environ["SESSION"]

# constant variable
chat_room_id = -1001374914057
bot_id = "@KOICA_test_bot"
sleep_time = 0.5


@pytest.mark.asyncio
async def test_check(client: TelegramClient):
    # Getting information about yourself

    reply = await get_reply_of_message_of_id(bot_id, "/check", client)
    assert "Here is your recent log info" in reply


@pytest.mark.asyncio
async def test_today(client: TelegramClient):
    # Getting information about yourself

    reply = await get_reply_of_message_of_id(bot_id, "/today", client)
    assert "Today's Logging" in reply


@pytest.mark.asyncio
async def test_logbook(client: TelegramClient):
    # Getting information about yourself

    reply = await get_reply_of_message_of_id(bot_id, "/로그북", client)
    assert reply == ""


@pytest.mark.asyncio
async def test_work_content(client: TelegramClient):
    # Getting information about yourself

    reply = await get_reply_of_message_of_id(bot_id, "/work_content", client)
    assert reply == ""


if __name__ == "__main__":
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
    client.connect()
    client.loop.run_until_complete(test_check(client))
    client.loop.run_until_complete(test_today(client))
    client.loop.run_until_complete(test_logbook(client))
    client.loop.run_until_complete(test_work_content(client))
    client.disconnect()
    client.disconnected
