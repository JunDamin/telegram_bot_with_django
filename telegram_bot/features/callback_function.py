from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from features.db_management import write_csv
from features.log import log_info
from features.data_IO import (
    get_logs_of_today,
    make_text_from_logs,
    get_logs_of_the_day,
    get_text_of_log_by_id,
    return_row,
    register_office,
)
from features.authority import private_only
from features.message import reply_markdown
from features.constant import LOG_COLUMN
from logs.models import Log, WorkContent
from staff.models import Member

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


@log_info()
def start(update, context):
    chat = update.message.chat
    if chat.type == "private":
        update.message.reply_text("Only in Group chat!")
        return None
    register_office(chat)
    update.message.reply_text("Office registered!")


@log_info()
def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


@log_info()
def get_logbook(update, context):
    """ Send a file when comamnd /signbook is issued"""
    logs = Log.objects.all()
    records = map(return_row, logs)
    header = [
        "id",
        "chat_id",
        "first_name",
        "last_name",
        "datetime",
        "category",
        "sub_category",
        "longitude",
        "latitude",
        "remarks",
        "confirmation",
    ]
    write_csv(records, header, "signing.csv")
    update.message.reply_document(document=open("signing.csv", "rb"))


@log_info()
def cancel(update, context):
    update.message.reply_message(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


@log_info()
def check_log(update, context):
    user = update.message.from_user
    member = Member.objects.get_or_none(id=user.id)
    logs = Log.objects.filter(member_fk=member).order_by("-created")[:5]

    header_message = "Here is your recent log info.\n"
    text_message = make_text_from_logs(logs, header_message)

    reply_markdown(update, context, text_message)


@log_info()
def get_a_log(update, context):
    log_id = context.user_data.get("log_id")
    if log_id:
        text_message = "You have been logged as below.\n"
        text_message += get_text_of_log_by_id(log_id)
        reply_markdown(update, context, text_message)

    else:
        update.message.reply_text("please send me a log id first.")
        context.user_data["status"] = "GET_LOG_ID"


def get_logs_today(update, context):
    """ """
    text_message = get_logs_of_today()
    reply_markdown(update, context, text_message)


@log_info()
def ask_date_for_log(update, context):

    text_message = "Please send the date as YYYY-MM-DD format"
    reply_markdown(update, context, text_message)
    context.user_data["status"] = "DATE_FOR_LOG"


def reply_logs_of_the_date(update, context):
    the_date = update.message.text
    import datetime.date as date

    try:
        text_message = get_logs_of_the_day(date.fromisoformat(the_date))
        reply_markdown(update, context, text_message)
        return True
    except ValueError:
        return False


@log_info()
def get_work_content_file(update, context):
    work_contents = WorkContent.objects.all()
    rows = [
        (
            work_content.id,
            work_content.content,
        )
        for work_content in work_contents
    ]
    write_csv(
        rows,
        [
            "id",
        ],
        "work_content.csv",
    )
    update.message.reply_document(document=open("work_content.csv", "rb"))


command_handlers = (
    CommandHandler("check", private_only(check_log)),
    CommandHandler("today", get_logs_today),
    MessageHandler(Filters.regex("^/로그북$"), private_only(get_logbook)),
    CommandHandler("work_content", private_only(get_work_content_file)),
    CommandHandler("start", start),
    CommandHandler("help", help_command),
)
