import pytz
from telegram import KeyboardButton
from telegram.ext import ConversationHandler
from conversations.text_message import *
from features.log import log_info
from features.data_IO import (
    check_status,
    put_sub_category,
    post_basic_user_data,
    make_text_from_logs,
    get_text_of_log_by_id,
    put_confirmation,
    get_record_by_log_id,
    delete_log_and_content,
    get_or_register_user,
    get_or_create_chat,
    save_log,
)
from features.message import (
    reply_markdown,
    set_context,
    set_location,
    get_log_id_and_record,
    send_initiating_message_by_branch,
    set_location_not_available,
)
from features.constant import LOG_COLUMN

# Sign in status
(ANSWER_WORKPLACE, ANSWER_LOG_DELETE, ANSWER_SIGN_IN_LOCATION, ANSWER_CONFIRMATION) = [
    "sign_in" + str(i) for i in range(4)
]


# Sign in Conv
@log_info()
def start_signing_in(update, context):

    # set variables and context
    user = update.message.from_user
    chat = update.message.chat
    log_datetime = update.message.date

    _chat = get_or_create_chat(chat.id, chat.type, chat.title)
    _user = get_or_register_user(_chat, user)
    log, is_exist = get_log_id_and_record(update, context, "signing in")
    logs = (log,)
    
    # set dictionary data

    data_dict = {
        "new": {
            "group_message": SIGN_IN_GROUP_MESSAGE.format(
                first_name=_user.frist_name, log_id=log.id, report_time=log.local_time
            ),
            "private_message": SIGN_IN_PRIVATE_MESSAGE.format(
                first_name=_user.first_name, log_id=log.id, report_time=log.local_time
            ),
            "keyboard": [
                ["Office", "Home"],
            ],
            "return": ANSWER_WORKPLACE,
        },
        "rewrite": {
            "group_message": make_text_from_logs(
                logs,
                REWRITE_HEADER,
            ),
            "private_message": make_text_from_logs(
                logs,
                REWRITE_HEADER,
                REWRITE_FOOTER,
            ),
            "keyboard": [
                ["Delete and Sign In Again", "SKIP"],
            ],
            "return": None,
        },
    }
    return send_initiating_message_by_branch(update, context, is_exist, data_dict)


@log_info()
def ask_confirmation_of_removal(update, context):
    log_id = context.user_data.get("log_id")
    if log_id:
        row = get_record_by_log_id(log_id)
        rows = (row,)
        header_message = f"Do you really want to do remove log No.{log_id}?\n"
        text_message = make_text_from_logs(rows, header_message)
        keyboard = [["REMOVE SIGN IN LOG", "NO"]]

        reply_markdown(update, context, text_message, keyboard)

        return ANSWER_LOG_DELETE
    else:
        text_message = "An Error has been made. Please try again."
        reply_markdown(update, context, text_message)
        return ConversationHandler.END


def override_log_and_ask_work_type(update, context):

    choices = {"REMOVE SIGN IN LOG": True, "NO": False}
    answer = choices.get(update.message.text)
    if answer:
        log_id = delete_log_and_content(update, context)

        text_message = f"Log No. {log_id} has been Deleted\n"
        reply_markdown(update, context, text_message)
    else:
        text_message = "process has been stoped. The log has not been deleted."
        reply_markdown(update, context, text_message)
        return ConversationHandler.END

    log = post_basic_user_data(update, context, "signing in")
    context.user_data["log_id"] = log.id
    return ask_sub_category(update, context)


def ask_sub_category(update, context):

    text_message = "Would you like to share where you work?"
    keyboard = [
        ["Office", "Home"],
    ]
    reply_markdown(update, context, text_message, keyboard)

    return ANSWER_WORKPLACE


@log_info()
def set_sub_category_and_ask_location(update, context):
    """Get sub category"""

    # save log work type data

    put_sub_category(context.user_data["log_id"], update.message.text)

    text_message = """I see! Please send me your location by click the button on your phone.
    1. Please check your location service is on.(if not please turn on your location service)
    2. Desktop app can not send location"""
    keyboard = [
        [KeyboardButton("Share Location", request_location=True), "Not Available"],
    ]
    reply_markdown(update, context, text_message, keyboard)
    return ANSWER_SIGN_IN_LOCATION


@log_info()
def set_sign_in_location_and_ask_confirmation(update, context):
    set_location_not_available(update, context)
    user_data = context.user_data

    HEADER_MESSAGE = "You have signed in as below. Do you want to confirm?"
    if set_location(update, context):
        text_message = HEADER_MESSAGE
        keyboard = [["Confirm", "Edit"]]
        text_message += get_text_of_log_by_id(user_data.get("log_id"))

        reply_markdown(update, context, text_message, keyboard)
        return ANSWER_CONFIRMATION
    else:
        return ConversationHandler.END


def confirm_the_data(update, context):
    choices = {"Confirm": True, "Edit": False}
    answer = choices.get(update.message.text)
    if answer:
        put_confirmation(update, context)
        context.user_data.clear()
        text_message = "Confirmed"
        reply_markdown(update, context, text_message)
        return ConversationHandler.END
    else:
        return ask_sub_category(update, context)
