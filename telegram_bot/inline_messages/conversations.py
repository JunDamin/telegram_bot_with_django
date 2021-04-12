from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
)

import inline_messages.half_day_off as half_day_off
import inline_messages.annual_leaves as annual_leave

SELECTING_ACTION, HALF_DAY, FULL_DAY, SHOWING, STOPPING, END = map(chr, range(6))


def start(update: Update, context: CallbackContext) -> str:
    """Select an action: Adding parent/child or show data."""
    text = (
        "You may choose to register day offs or end the",
        "conversation. To abort, simply type /stop.",
    )

    buttons = [
        [
            InlineKeyboardButton(text="Add half-day off", callback_data=str(HALF_DAY)),
            InlineKeyboardButton(text="Add annual leave", callback_data=str(FULL_DAY)),
        ],
        [
            InlineKeyboardButton(text="Show data", callback_data=str(SHOWING)),
            InlineKeyboardButton(text="Done", callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.message.reply_text(text=text, reply_markup=keyboard)

    return SELECTING_ACTION


def stop(update: Update, _: CallbackContext) -> int:
    """End Convresation by command."""
    update.message.reply_text("Okay, bye.")

    return ConversationHandler.END


def handle_selection(update, context):
    data = update.callback_query.data
    if data == f"{HALF_DAY}":
        half_day_off.start(update, context)
        return HALF_DAY
    if data == f"{FULL_DAY}":
        annual_leave.start(update, context)
        return FULL_DAY


selection_handlers = [
    CallbackQueryHandler(handle_selection, pattern=f"^{HALF_DAY}|{FULL_DAY}$"),
]

inline_convs = [
    ConversationHandler(
        entry_points=[CommandHandler("leave", start)],
        states={
            SELECTING_ACTION: selection_handlers,
            HALF_DAY: [half_day_off.half_day_off_conv],
            FULL_DAY: [annual_leave.annual_leave_conv],
            STOPPING: [CommandHandler("start", start)],
        },
        fallbacks=[CommandHandler("stop", stop)],
        allow_reentry=True,
    )
]
