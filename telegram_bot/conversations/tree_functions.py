import re
from math import sqrt
from features.log import log_info
from features.data_IO import (
    register_office,
    get_or_register_user,
    save_log,
    get_or_none_log_of_date,
    make_text_from_logs,
    get_log_by_id,
    put_sub_category,
    put_confirmation,
    post_work_content,
)
from conversations.text_message import (
    start_regex,
    init_group_message,
    reply_keyboard,
    yes_dict,
    optional_status_message,
    optional_status_keyboard,
    REWRITE_HEADER,
    REWRITE_FOOTER,
    ASK_REMOVAL_CONFIRMATION,
    INFO_REMOVAL,
    ASK_LOCATION_TEXT,
    ASK_LOCATION_KEYBOARD,
    ASK_LOG_CONFIRMATION_TEXT,
    ASK_LOG_CONFIRMATION_KEYBOARD,
    ASK_WORK_CONTENT,
    CHECK_CONTENT_TEXT,
    CHECK_CONTENT_KEYBOARD,
)
from features.message import (
    send_markdown,
    reply_markdown,
    set_location_not_available,
    set_location,
    initiate_private_conversation,
)


def set_session(update, context):
    text = update.message.text

    for status in start_regex:
        m = re.search(start_regex.get(status), text, re.IGNORECASE)
        if m:
            context.user_data["session"] = status
            return status
    return None

def clear_session(udpate, context):
    context.user_data.clear()

def is_late(update, context):
    message_datetime = update.message.date
    status = set_session(update, context)
    chat = update.message.chat
    user = update.message.from_user
    member = get_or_register_user(chat, user)
    open_time = member.office_fk.open_time
    return (
        status == "signing in"
        and message_datetime.astimezone(member.office_fk.timezone).time() > open_time
    )