import re
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, Filters, CommandHandler
from features.authority import public_only, private_only, self_only
from conversations import (
    set_remarks,
    remove_log,
    edit_log,
)


def cancel(update, context):
    update.message.reply_text("Bye!", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


cancel_handler = MessageHandler(Filters.regex("^SKIP$"), cancel)

# set remarks

set_remarks_conv = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex("/비고작성"), private_only(set_remarks.ask_log_id_for_remarks)
        )
    ],
    states={
        set_remarks.HANDLE_REMARKS_LOG_ID: [
            MessageHandler(
                Filters.regex("[0-9]*") & Filters.private,
                set_remarks.ask_content_for_remarks,
            ),
        ],
        set_remarks.HANDLE_REMARKS_CONTENT: [
            MessageHandler(Filters.text & Filters.private, set_remarks.set_remarks),
        ],
    },
    fallbacks=[MessageHandler(Filters.regex("^SKIP$"), cancel)],
    map_to_parent={},
    allow_reentry=True,
)


# delete log conversation

# add handlers from conversation
conversation_handlers = (
    set_remarks_conv,
    cancel_handler,
)
