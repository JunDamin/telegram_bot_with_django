from datetime import time, date
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    CallbackContext,
)
from telegram import Update

from logs.models import HalfDayOff
from staff.models import Member
from inline_messages.telegramcalendar import (
    process_half_day_off,
    create_half_day_options,
    separate_callback_data,
)


SELECT_OPTION = "SELECT_OPTION"


def start(update, context):
    text, keyboard = create_half_day_options(update, context)
    update.message.reply_text(
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
        time_schedule = {
            "Morning": (
                time(8, 0),
                time(12, 0),
            ),
            "Afternoon": (time(13, 00), time(16, 30)),
        }
        start, end = time_schedule.get(off_type)
        save_halfdayoff(member, off_date, start, end)
        update.callback_query.edit_message_text(
            text=text,
        )
        context.user_data.clear()
        return ConversationHandler.END
    return SELECT_OPTION


half_day_off_conv = ConversationHandler(
    entry_points=[CommandHandler("halfdayoff", start)],
    states={
        SELECT_OPTION: [CallbackQueryHandler(inline_handler, pattern="^.*")],
    },
    fallbacks=[CommandHandler("stop", stop)],
)


def save_halfdayoff(member_fk, offdate, start, end, confirmed=True) -> None:
    dayoff = HalfDayOff(
        member_fk=member_fk, date=offdate, start=start, end=end, confirmed=confirmed
    )
    dayoff.save()
