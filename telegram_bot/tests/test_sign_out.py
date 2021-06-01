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
async def test_sign_out_check(client: TelegramClient):
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

    # ... get back Test
    reply = await get_reply_of_message_of_id(bot_id, "SKIP", client)
    reply = await get_reply_of_message_of_id(chat_room_id, "sign out", client)
    reply = await get_reply_of_message_of_id(bot_id, "", client)

    m = re.search(r"Log No.(\d+)", reply)
    if m:
        log_id = m.group(1)
        await erase_log(bot_id, str(log_id), client)


@pytest.mark.asyncio
async def test_sign_out_first(client: TelegramClient):
    sleep(sleep_time)
    # Getting information about yourself

    # ...Get back Test
    reply = await get_reply_of_message_of_id(chat_room_id, "sign out", client)
    m = re.search(r"Log No.(\d+)", reply)
    reply = await get_reply_of_message_of_id(bot_id, "", client)

    if m:
        log_id = m.group(1)
        print(log_id)

    # conversation
    async with client.conversation(bot_id) as conv:

        sleep(sleep_time)

        qna = [
            ("Office", "I see"),
            ("Not Available", "You have logged as below."),
            ("Confirm", "Confirmed"),
        ]

        await check_assert_with_qna(qna, conv)


@pytest.mark.asyncio
async def test_sign_out_rewrite(client: TelegramClient):

    sleep(sleep_time)
    # Getting information about yourself

    # ...Get back Test
    reply = await get_reply_of_message_of_id(chat_room_id, "sign out", client)
    reply = await get_reply_of_message_of_id(bot_id, "", client)

    sleep(sleep_time)
    # Signing Out conversation
    async with client.conversation(bot_id) as conv:

        qna = [
            ("Rewrite the log", "Do you really want to do remove log No."),
            ("Yes, I delete and write again", "You have relogged as below."),
            ("Home", "I see"),
            ("Not Available", "You have logged as below. Do you want to confirm"),
            (
                "Send content of today",
                "Please text me the today's work.",
            ),
            ("It is a test", "Content of Work"),
            ("Save content", "Content has been saved"),
            ("Confirm", "Confirmed"),
        ]

        log_id = await check_assert_with_qna(qna, conv)

    # earase log after use
    await erase_log(bot_id, str(log_id), client)


@pytest.mark.asyncio
async def test_sign_out_report(client: TelegramClient):
    sleep(sleep_time)
    # Getting information about yourself

    # ...Get back Test
    reply = await get_reply_of_message_of_id(chat_room_id, "sign out", client)
    reply = await get_reply_of_message_of_id(bot_id, "", client)

    # conversation
    async with client.conversation(bot_id) as conv:

        sleep(sleep_time)

        qna = [
            ("Home", "I see"),
            ("Not Available", "You have logged as below."),
            (
                "Send content of today",
                "Please text me the today's work.",
            ),
            ("It is a test", "Content of Work"),
            ("Save content", "Content has been saved"),
            ("Confirm", "Confirmed"),
        ]

        await check_assert_with_qna(qna, conv)


@pytest.mark.asyncio
async def test_sign_out_edit(client: TelegramClient):

    # Getting information about yourself

    # ...Get back Test
    reply = await get_reply_of_message_of_id(chat_room_id, "sign out", client)
    reply = await get_reply_of_message_of_id(bot_id, "", client)

    # Signing in conversation
    async with client.conversation(bot_id) as conv:

        qna = [
            ("Home", "I see"),
            ("Not Available", "You have logged as below."),
            (
                "Send content of today",
                "Please text me the today's work.",
            ),
            ("It is a test", "Content of Work"),
            ("Save content", "Content has been saved"),
            ("Go back", "Where do you work?"),
            ("Office", "I see"),
            ("Not Available", "You have logged as below. Do you want to confirm"),
            ("Confirm", "Confirmed"),
            ("/work_content", ""),
        ]

        log_id = await check_assert_with_qna(qna, conv)

        # earase log after use
        await erase_log(bot_id, str(log_id), client)
