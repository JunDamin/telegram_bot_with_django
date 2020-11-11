from telegram import KeyboardButton
from telegram.ext import ConversationHandler
from features.log import log_info
from features.data_IO import (
    post_basic_user_data,
    make_text_from_logs,
    get_text_of_log_by_id,
    put_confirmation,
    post_work_content,
    delete_log_and_content,
    delete_content,
    get_record_by_log_id,
    get_or_create_chat,
    get_or_register_user,
    set_user_context,
    put_sub_category
)
from conversations.text_message import *
from features.message import (
    reply_markdown,
    set_location,
    get_log_id_and_record,
    send_initiating_message_by_branch,
    set_location_not_available,
)
from features.constant import LOG_COLUMN

# Sign out
(
    ANSWER_WORK_TYPE,
    ANSWER_WORK_CONTENT,
    ANSWER_CONTENT_CONFIRMATION,
    ANSWER_LOG_DELETE,
    ANSWER_SIGN_OUT_LOCATION,
    ANSWER_CONFIRMATION,
) = ["sign_out" + str(i) for i in range(6)]


# Sign out conv
@log_info()
def start_signing_out(update, context):

    # set variables and context
    user = update.message.from_user
    chat = update.message.chat
    status = "signing out"

    _chat = get_or_create_chat(chat.id, chat.type, chat.title)
    _user = get_or_register_user(_chat, user)
    log, is_exist = get_log_id_and_record(update, context, status)
    logs = (log,)

    set_user_context(update, context, log)

    # set dictionary data

    data_dict = {
        "new": {
            "group_message": SIGN_OUT_GROUP_MESSAGE.format(
                first_name=_user.first_name, log_id=log.id, report_time=log.local_time()
            ),
            "private_message": SIGN_OUT_PRIVATE_MESSAGE.format(
                first_name=_user.first_name, log_id=log.id, report_time=log.local_time()
            ),
            "keyboard": [
                [
                    "I worked at Office",
                    "I worked at home(I summit daily report)",
                ]
            ],
            "return": ANSWER_WORK_TYPE,
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
                ["Delete and Sign Out Again", "SKIP"],
            ],
            "return": None,
        },
    }
    return send_initiating_message_by_branch(update, context, is_exist, data_dict)


@log_info()
def ask_confirmation_of_removal(update, context):
    log_id = context.user_data.get("log_id")
    if log_id:
        log = get_record_by_log_id(log_id)
        logs = (log,)
        header_message = ASK_REMOVAL_CONFIRMATION.format(log_id=log_id)
        text_message = make_text_from_logs(logs, header_message)
        keyboard = [["REMOVE SIGN OUT LOG", "NO"]]

        reply_markdown(update, context, text_message, keyboard)

        return ANSWER_LOG_DELETE
    else:
        text_message = ERROR_MESSAGE
        reply_markdown(update, context, text_message)
        return ConversationHandler.END


def override_log(update, context):

    choices = {"REMOVE SIGN OUT LOG": True, "NO": False}
    answer = choices.get(update.message.text)
    if answer:
        log_id = delete_log_and_content(update, context)
        text_message = INFO_REMOVAL.format(log_id=log_id)
        reply_markdown(update, context, text_message)
    else:
        text_message = STOP_REMOVAL
        reply_markdown(update, context, text_message)
        return ConversationHandler.END
    log = post_basic_user_data(update, context, "signing out")
    context.user_data["log_id"] = log.id
    return ask_work_type(update, context)


def ask_sign_out_location(update, context):

    check_branch = {
        "I worked at Office": "Office",
        "I worked at home(I summit daily report)": "Home",
    }
    optional_status = check_branch.get(update.message.text)
    is_office = optional_status == "Office"
    log_id = context.user_data.get("log_id")
    put_sub_category(log_id, optional_status)

    log = get_record_by_log_id(log_id)
    is_delete = is_office and hasattr(log, "work_content")
    if is_delete:
        work_content = log.work_content
        work_content.delete()


    text_message = ASK_LOCATION
    keyboard = [
        [KeyboardButton("Share Location", request_location=True), "Not Available"],
    ]

    reply_markdown(update, context, text_message, keyboard)

    return ANSWER_SIGN_OUT_LOCATION


@log_info()
def set_sign_out_location(update, context):
    set_location_not_available(update, context)
    user_data = context.user_data
    HEADER_MESSAGE = ASK_SIGN_OUT_CONFIRMATION
    if set_location(update, context):
        text_message = HEADER_MESSAGE
        keyboard = [["Confirm", "Edit"]]
        text_message += get_text_of_log_by_id(user_data.get("log_id"))

        reply_markdown(update, context, text_message, keyboard)

        return ANSWER_CONFIRMATION
    else:
        return ConversationHandler.END


def confirm_the_data(update, context):
    print("test")
    choices = {"Confirm": True, "Edit": False}
    answer = choices.get(update.message.text)
    if answer:
        put_confirmation(update, context)
        context.user_data.clear()
        text_message = "Confirmed"
        reply_markdown(update, context, text_message)
        return ConversationHandler.END
    else:
        return ask_work_type(update, context)


def ask_work_type(update, context):
    text_message = ASK_WORK_TYPE
    keyboard = [
        ["I worked at Office", "I worked at home(I summit daily report)"]
    ]

    reply_markdown(update, context, text_message, keyboard)

    return ANSWER_WORK_TYPE


@log_info()
def ask_work_content(update, context):

    text_message = ASK_WORK_CONTENT
    reply_markdown(update, context, text_message)

    return ANSWER_WORK_CONTENT


@log_info()
def check_work_content(update, context):

    answer = update.message.text

    context.user_data["work_content"] = answer
    text_message = CHECK_CONTENT.format(answer=answer)
    keyboard = [["YES", "NO"]]
    reply_markdown(update, context, text_message, keyboard)

    return ANSWER_CONTENT_CONFIRMATION


@log_info()
def save_content_and_ask_location(update, context):
    content = context.user_data.get("work_content")
    post_work_content(update, context, content)

    return ask_sign_out_location(update, context)
