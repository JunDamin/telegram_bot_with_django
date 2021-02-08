import os
import pytest
import re
from time import sleep
from telethon import TelegramClient
from common_parts import (
    get_reply_of_message_of_id,
    erase_log,
    check_assert_with_qna,
    chat_room_id,
    bot_id,
    sleep_time,
)

# Your API ID, hash and session string here
api_id = int(os.environ["APP_ID"])
api_hash = os.environ["APP_HASH"]
session_str = os.environ["SESSION"]


@pytest.mark.asyncio
async def test_sign_in_check(client: TelegramClient):
    # Getting information about yourself

    me = await client.get_me()

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    username = me.username
    print(username)
    print(me.phone)

    # You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
        print(dialog.name, "has ID", dialog.id)

    # ...Sign In Test
    reply = await get_reply_of_message_of_id(bot_id, "SKIP", client)
    reply = await get_reply_of_message_of_id(chat_room_id, "sign in", client)
    reply = await get_reply_of_message_of_id(bot_id, "", client)
    m = re.search(r"Log No.(\d+)", reply)
    if m:
        log_id = m.group(1)
        await erase_log(bot_id, str(log_id), client)


@pytest.mark.asyncio
async def test_sign_in_first(client: TelegramClient):
    sleep(sleep_time)
    # Getting information about yourself
    reply = await get_reply_of_message_of_id(chat_room_id, "sign in", client)
    reply = await get_reply_of_message_of_id(bot_id, "", client)

    m = re.search(r"Log No.(\d+)", reply)
    if m:
        log_id = m.group(1)
        print(log_id)

    # Signing in conversation
    async with client.conversation(bot_id) as conv:

        sleep(sleep_time)

        qna = [
            ("Office", "I see"),
            ("Not Available", "You have logged as below. Do you want to confirm"),
            ("Confirm", "Confirmed"),
        ]

        await check_assert_with_qna(qna, conv)


@pytest.mark.asyncio
async def test_sign_in_rewrite(client: TelegramClient):

    sleep(sleep_time)
    # ...Sign In Test
    reply = await get_reply_of_message_of_id(chat_room_id, "sign in", client)
    reply = await get_reply_of_message_of_id(bot_id, "", client)

    m = re.search(r"Log No.(\d+)", reply)
    if m:
        log_id = m.group(1)
    sleep(sleep_time)

    # Signing in conversation
    async with client.conversation(bot_id) as conv:

        qna = [
            ("Delete and Rewrite", "Do you really want to do remove log No."),
            ("Remove the log", "has been Deleted"),
        ]

        await check_assert_with_qna(qna, conv)

        response = await conv.get_response()
        print(response.text)
        assert "Would you like to share where you work" in response.text

        qna = [
            ("Office", "I see"),
            ("Not Available", "You have logged as below. Do you want to confirm"),
            ("Confirm", "Confirmed"),
        ]

        log_id = await check_assert_with_qna(qna, conv)

    # earase log after use
    await erase_log(bot_id, str(log_id), client)


@pytest.mark.asyncio
async def test_sign_in_edit(client: TelegramClient):
    sleep(sleep_time)
    # Getting information about yourself

    # ...Sign In Test
    reply = await get_reply_of_message_of_id(chat_room_id, "sign in", client)
    reply = await get_reply_of_message_of_id(bot_id, "", client)

    # Signing in conversation
    async with client.conversation(bot_id) as conv:

        qna = [
            ("Office", "I see"),
            ("Not Available", "You have logged as below. Do you want to confirm"),
            ("Edit", "Would you like to share where you work"),
            ("Office", "I see"),
            ("Not Available", "You have logged as below. Do you want to confirm"),
            ("Confirm", "Confirmed"),
        ]

        log_id = await check_assert_with_qna(qna, conv)

        # earase log after use
        await erase_log(bot_id, str(log_id), client)
