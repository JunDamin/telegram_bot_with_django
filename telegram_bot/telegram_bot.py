import os
from collections import deque
from telegram.ext import Updater
from features.callback_function import command_handlers
from conversations.conversation import conversation_handlers
from inline_messages.conversations import inline_convs

# Bot setting
token = os.getenv("TOKEN")
print("telegram bot started")


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram

    deque(map(dp.add_handler, command_handlers))
    # on messages handling i.e message - set callback function for each message keywords

    # add hander from conversations
    deque(map(dp.add_handler, conversation_handlers))
    deque(map(dp.add_handler, inline_convs))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
