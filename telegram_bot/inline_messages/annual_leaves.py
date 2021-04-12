from datetime import date
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    CallbackContext,
)
from logs.models import Leave
from staff.models import Member
from telegram import Update

from inline_messages.telegramcalendar import (
    create_full_day_options,
    process_full_day_off,
    separate_callback_data,
)


SELECT_OPTION, START_DATE, END_DATE = map(lambda x: "f"+chr(x), range(3))


def start(update, context):
    text, keyboard = create_full_day_options(update, context)
    update.callback_query.edit_message_text(
        text=text,
        reply_markup=keyboard,
    )
    return SELECT_OPTION


def stop(update: Update, _: CallbackContext) -> int:
    """End Convresation by command."""
    update.message.reply_text("Okay, bye.")

    return ConversationHandler.END


# start_date end_date를 context에 저장하는 것
def inline_handler(update, context):
    selected, offdate = process_full_day_off(update, context)
    text, keyboard = create_full_day_options(update, context)
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
        start_date = context.user_data.get("Start date")
        end_date = context.user_data.get("End date")
        text = f"{user.name}'s annual leave from {start_date} to {end_date} \nhas been registered."
        member = Member.objects.get_or_none(id=user.id)
        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)

        leave_days = 1

        save_leave(member, start_date, end_date, leave_days)
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


def save_leave(member_fk, start_date, end_date, leave_days):
    annual_leave = Leave(
        member_fk=member_fk, leave_type="Full", start_date=start_date, end_date=end_date
    )
    annual_leave.save()


annual_leave_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(inline_handler, pattern="^.*$")],
    states={
        SELECT_OPTION: [CallbackQueryHandler(inline_handler, pattern="^.*")],
    },
    fallbacks=[CommandHandler("stop", stop)],
)
