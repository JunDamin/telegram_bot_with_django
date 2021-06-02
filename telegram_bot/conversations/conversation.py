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

remove_log_conv = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex("/로그삭제"), private_only(remove_log.ask_log_id_to_remove)
        )
    ],
    states={
        remove_log.HANDLE_DELETE_LOG_ID: [
            MessageHandler(
                Filters.regex("[0-9]*") & Filters.private,
                remove_log.ask_confirmation_of_removal,
            ),
        ],
        remove_log.HANDLE_LOG_DELETE: [
            MessageHandler(
                Filters.regex("^YES$|^NO$") & Filters.private, remove_log.remove_log
            ),
        ],
    },
    fallbacks=[MessageHandler(Filters.regex("^SKIP$"), cancel)],
    map_to_parent={},
    allow_reentry=True,
)


edit_log_conv = ConversationHandler(
    entry_points=[CommandHandler("edit", private_only(edit_log.ask_log_id_to_edit))],
    states={
        edit_log.ANSWER_LOG_ID: [
            MessageHandler(
                Filters.regex("[0-9,\s]*") & Filters.private,
                edit_log.ask_confirmation_of_edit,
            ),
        ],
        edit_log.ANSWER_CONFIRMATION: [
            MessageHandler(
                Filters.regex("^YES$|^NO$") & Filters.private,
                self_only(edit_log.start_edit),
            ),
        ],
    },
    fallbacks=[MessageHandler(Filters.regex("^SKIP$"), cancel)],
    map_to_parent={},
    allow_reentry=True,
)


# add handlers from conversation
conversation_handlers = (
    set_remarks_conv,
    remove_log_conv,
    edit_log_conv,
    cancel_handler,
)
