from telegram import KeyboardButton
from telegram.ext import ConversationHandler
from conversations.text_message import *
from features.log import log_info
from features.data_IO import (
    put_sub_category,
    post_basic_user_data,
    make_text_from_logs,
    get_text_of_log_by_id,
    put_confirmation,
    get_record_by_log_id,
    delete_log_and_content,
    get_or_register_user,
    get_or_create_chat,
    set_user_context,
)
from features.message import (
    reply_markdown,
    set_location,
    get_log_id_and_record,
    send_initiating_message_by_branch,
    set_location_not_available,
)

# Lunch break
ANSWER_LOG_DELETE, ANSWER_LUNCH_TYPE, ANSWER_LUNCH_LOCATION, ANSWER_CONFIRMATION = [
    "get_back" + str(i) for i in range(4, 8)
]


@log_info()
def get_back_to_work(update, context):

    # set variables and context
    user = update.message.from_user
    chat = update.message.chat
    status = "getting back"

    _chat = get_or_create_chat(chat.id, chat.type, chat.title)
    _user = get_or_register_user(_chat, user)
    log, is_exist = get_log_id_and_record(update, context, status)
    logs = (log,)

    set_user_context(update, context, log)

    "Please check my DM(Direct Message) to you" ""

    data_dict = {
        "new": {
            "group_message": GET_BACK_GROUP_MESSAGE.format(
                first_name=_user.first_name, log_id=log.id, report_time=log.local_time()
            ),
            "private_message": GET_BACK_PRIVATE_MESSAGE.format(
                first_name=_user.first_name, log_id=log.id, report_time=log.local_time()
            ),
            "keyboard": [
                ["Without any member of KOICA", "With KOICA Colleagues"],
            ],
            "return": ANSWER_LUNCH_TYPE,
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
                ["Delete and Get Back to Work Again", "SKIP"],
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
        header_message = ASK_REMOVAL_CONFIRMATION.format(log_id=log_id)
        text_message = make_text_from_logs(rows, header_message)
        keyboard = [["REMOVE GET BACK LOG", "NO"]]

        reply_markdown(update, context, text_message, keyboard)
        return ANSWER_LOG_DELETE
    else:
        text_message = ERROR_MESSAGE
        reply_markdown(update, context, text_message)
        return ConversationHandler.END


def override_log_and_ask_lunch_type(update, context):

    choices = {"REMOVE GET BACK LOG": True, "NO": False}
    answer = choices.get(update.message.text)
    if answer:
        log_id = delete_log_and_content(update, context)

        text_message = INFO_REMOVAL.format(log_id=log_id)
        reply_markdown(update, context, text_message)

    else:
        text_message = STOP_REMOVAL
        reply_markdown(update, context, text_message)

        return ConversationHandler.END

    log = post_basic_user_data(update, context, "getting back")
    context.user_data["log_id"] = log.id
    return ask_lunch_type(update, context)


@log_info()
def ask_lunch_type(update, context):
    text_message = ASK_GET_BACK_INFO
    keyboard = [
        ["Without any member of KOICA", "With KOICA Colleagues"],
    ]
    reply_markdown(update, context, text_message, keyboard)
    return ANSWER_LUNCH_TYPE


@log_info()
def set_lunch_type_and_ask_lunch_location(update, context):
    """  """
    # save log work type data
    put_sub_category(context.user_data["log_id"], update.message.text)
    text_message = ASK_LOCATION
    keyboard = [
        [KeyboardButton("Share Location", request_location=True), "Not Available"],
    ]
    reply_markdown(update, context, text_message, keyboard)
    return ANSWER_LUNCH_LOCATION


@log_info()
def set_lunch_location_and_ask_confirmation(update, context):
    set_location_not_available(update, context)
    user_data = context.user_data
    HEADER_MESSAGE = ASK_GET_BACK_CONFIRMATION
    if set_location(update, context):
        text_message = HEADER_MESSAGE
        text_message += get_text_of_log_by_id(user_data.get("log_id"))
        keyboard = [["Confirm", "Edit"]]
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
        return ask_lunch_type(update, context)
