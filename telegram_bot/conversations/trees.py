from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, Filters
from conversations.sign_in_out import sign_in_tree, sign_out_tree
from conversations.get_back import get_back_tree
from conversations.edit_log import edit_tree
from conversations.remove_log import remove_tree
from conversations.set_remarks import remarks_tree


def cancel(update, context):
    update.message.reply_text("Bye!", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


cancel_handler = MessageHandler(Filters.regex("^SKIP$"), cancel)

conversations = [
    cancel_handler,
    sign_in_tree.get_conversation(),
    sign_out_tree.get_conversation(),
    get_back_tree.get_conversation(),
    edit_tree.get_conversation(),
    remove_tree.get_conversation(),
    remarks_tree.get_conversation(),
]
