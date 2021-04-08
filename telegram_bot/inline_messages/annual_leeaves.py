import logging

from telegram.ext import (
    Updater,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    CallbackContext,
)
from telegram import ReplyKeyboardRemove, Update

from telegramcalendar import (
    create_leave_form,
    input_annual_leave,
)


TOKEN = "1085920737:AAE8qnQCdRQRswV1dvNEDnRitnDHY0s7hNQ"

LEAVE_FORM, START_DATE, END_DATE = map(chr, range(3))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start_leave_form(update, context):
    start_date = context.user_data.get("START_DATE")
    end_date = context.user_data.get("END_DATE")

    update.message.reply_text(
        "Please set dates and confirm",
        reply_markup=create_leave_form(start_date, end_date),
    )

    if "CONFRIM":
        save_annual_leave(update, context)
        text "annual leave has been saved as below."
        text += f"\nName : {update.messge.from_user.name}"
        text += f"\nStart Date: {start_date}"
        text += f"\nEnd Date: {end_date}"
        update.callback_query.edit_message(text=text)


def stop(update: Update, _: CallbackContext) -> int:
    """End Convresation by command."""
    update.message.reply_text("Okay, bye.")

    return ConversationHandler.END


def inline_handler(update, context):
    selected, date = input_annual_leave(update, context)
    if selected:
        context.bot.send_message(
            chat_id=update.callback_query.message.chat.id,
            text="You selected %s" % (date.strftime("%d/%m/%Y")),
            reply_markup=ReplyKeyboardRemove(),
        )
    return LEAVE_FORM


def save_annual_leave(update, context):
    """Connect to the DB"""
    return ""


annual_leave_conv = ConversationHandler(
    entry_points=[CommandHandler("leave", start_leave_form)],
    states={
        LEAVE_FORM: [CallbackQueryHandler(start_leave_form)],
        START_DATE: [CallbackQueryHandler(inline_handler)],
        END_DATE: [CallbackQueryHandler(inline_handler)],
    },
    fallbacks=[CommandHandler("stop", stop)],
)


if TOKEN == "":
    print("Please write TOKEN into file")
else:
    up = Updater(TOKEN)

    up.dispatcher.add_handler(CommandHandler("leave", start_leave_form))
    up.dispatcher.add_handler(CallbackQueryHandler(inline_handler))

    up.start_polling()
    up.idle()
