from datetime import date
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    CallbackContext,
)
from telegram import Update

from logs.models import Leave
from staff.models import Member
from inline_messages.telegramcalendar import (
    process_half_day_off,
    create_half_day_options,
    separate_callback_data,
)


SELECT_OPTION = "SELECT_OPTION"


def start(update, context):
    print("halfday")
    text, keyboard = create_half_day_options(update, context)
    update.callback_query.edit_message_text(
        text=text,
        reply_markup=keyboard,
    )
    return SELECT_OPTION


def stop(update: Update, _: CallbackContext) -> int:
    """End Convresation by command."""
    update.message.reply_text("Okay, bye.")

    return ConversationHandler.END


def inline_handler(update, context):
    selected, offdate = process_half_day_off(update, context)
    text, keyboard = create_half_day_options(update, context)
    print(selected, offdate)
    if selected:
        update.callback_query.edit_message_text(
            text=text,
            reply_markup=keyboard,
        )
    query = update.callback_query
    (action, data) = separate_callback_data(query.data)
    if action == "CONFIRM":
        user = query.from_user
        off_type = context.user_data.get("off_type")
        off_date = context.user_data.get("date")
        text = f"{user.name} {off_type} off on {off_date} \nhas been registered."
        member = Member.objects.get_or_none(id=user.id)
        off_date = date.fromisoformat(off_date)
        save_halfdayoff(member, off_type, off_date)
        update.callback_query.edit_message_text(
            text=text,
        )
        context.user_data.clear()
        return ConversationHandler.END
    if action == "CANCEL":
        text = "OK. Good bye."
        update.callback_query.edit_message_text(
            text=text,
        )
        context.user_data.clear()
        return ConversationHandler.END
    return SELECT_OPTION


half_day_off_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(inline_handler, pattern="^.*$")],
    states={
        SELECT_OPTION: [CallbackQueryHandler(inline_handler, pattern="^.*")],
    },
    fallbacks=[CommandHandler("stop", stop)],
)


def save_halfdayoff(member_fk, leave_type, offdate, confirmed=False) -> None:
    dayoff = Leave(
        member_fk=member_fk, leave_type=leave_type, start_date=offdate, end_date=offdate, confirmed=confirmed
    )
    dayoff.save()
