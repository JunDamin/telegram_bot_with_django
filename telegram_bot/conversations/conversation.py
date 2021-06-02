import re
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, Filters, CommandHandler


def cancel(update, context):
    update.message.reply_text("Bye!", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


cancel_handler = MessageHandler(Filters.regex("^SKIP$"), cancel)

# add handlers from conversation
conversation_handlers = (
    cancel_handler,
)
