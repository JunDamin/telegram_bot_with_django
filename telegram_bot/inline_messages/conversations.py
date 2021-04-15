from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
)
from datetime import date
from staff.models import Member
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


def selelct_option(update: Update, context: CallbackContext) -> str:
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

    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return SELECTING_ACTION


def stop(update: Update, _: CallbackContext) -> int:
    """End Convresation by command."""
    update.message.reply_text("Okay, bye.")

    return ConversationHandler.END


def show(update, context):
    """ """
    print("show work")
    query = update.callback_query
    user = query.from_user
    member = Member.objects.get_or_none(id=user.id)
    year = date.today().year
    leaves = member.leaves.filter(end_date__gte=date(year, 1, 1))
    text = (
        f"You have registerd {len(leaves)} leaves within this year.",
        "Please check the list below.\n",
    )
    for leave in leaves:
        leave_date = leave.start_date.strftime("%Y.%m.%d") + (
            (" - " + leave.end_date.strftime("%Y.%m.%d"))
            if leave.leave_type == "Full"
            else ""
        )
        text += (f"id : {leave.id} | {leave.leave_type} | {leave_date}\n",)

    text = "\n".join(text)
    buttons = [
        [
            InlineKeyboardButton(text="Go back", callback_data=str(SELECTING_ACTION)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return SELECTING_ACTION


def handle_selection(update, context):
    data = update.callback_query.data
    print("What happened?", data)
    if data == f"{HALF_DAY}":
        half_day_off.start(update, context)
        return HALF_DAY
    if data == f"{FULL_DAY}":
        annual_leave.start(update, context)
        return FULL_DAY
    if data == f"{SHOWING}":
        show(update, context)
        return SHOWING
    if data == f"{SELECTING_ACTION}":
        selelct_option(update, context)
        return SELECTING_ACTION
    if data == f"{END}":
        text = "Ok. Bye."
        update.callback_query.edit_message_text(text=text)
        return ConversationHandler.END


selection_handlers = [
    CallbackQueryHandler(
        handle_selection,
        pattern=f"^{HALF_DAY}|{FULL_DAY}|{SHOWING}|{END}$",
    ),
]

inline_convs = [
    ConversationHandler(
        entry_points=[CommandHandler("leave", start)],
        states={
            SELECTING_ACTION: selection_handlers,
            SHOWING: [
                CallbackQueryHandler(handle_selection, pattern=f"^{SELECTING_ACTION}$")
            ],
            HALF_DAY: [half_day_off.half_day_off_conv],
            FULL_DAY: [annual_leave.annual_leave_conv],
            STOPPING: [CommandHandler("start", start)],
        },
        fallbacks=[CommandHandler("stop", stop)],
        allow_reentry=True,
    )
]
