import logging

from telegram.ext import Updater
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardRemove


from telegramcalendar import process_calendar_selection, create_leave_form


TOKEN = "1085920737:AAE8qnQCdRQRswV1dvNEDnRitnDHY0s7hNQ"


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start_leave_form(update, context):
    update.message.reply_text(
        "Please set dates and confirm", reply_markup=create_leave_form("annual_leave", 0, 0)
    )


def inline_handler(update, context):
    selected, date = process_calendar_selection(update, context)
    if selected:
        context.bot.send_message(
            chat_id=update.callback_query.message.chat.id,
            text="You selected %s" % (date.strftime("%d/%m/%Y")),
            reply_markup=ReplyKeyboardRemove(),
        )


if TOKEN == "":
    print("Please write TOKEN into file")
else:
    up = Updater(TOKEN)

    up.dispatcher.add_handler(CommandHandler("leave", start_leave_form))
    up.dispatcher.add_handler(CallbackQueryHandler(inline_handler))

    up.start_polling()
    up.idle()
