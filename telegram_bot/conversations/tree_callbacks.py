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

from conversations.tree_functions import clear_session, set_session, is_late


@log_info()
def cancel(update, context):
    clear_session(update, context)
    return {"message": "OK. Good bye!"}


@log_info()
def sign_in_init(update, context):
    # set variable
    chat = update.message.chat
    user = update.message.from_user

    # check chat and user
    register_office(chat)
    member = get_or_register_user(chat, user)

    # set session and log
    status = set_session(update, context)
    message_datetime = update.message.date
    late = is_late(update, context)
    log = get_or_none_log_of_date(member, message_datetime.date(), status)
    new = False if log else True
    if new:
        log = save_log(member, update.message.date, status)
    context.user_data["log_id"] = log.id

    # make text by session
    text = init_group_message.get(status)

    # Make a branch
    if late:
        texts = text.split("\n")
        texts.insert(1, "You have been late.\n")
        text = "\n".join(texts)

    reply_message = (
        text.format(
            first_name=user.first_name, log_id=log.id, report_time=log.local_time()
        )
        if new
        else make_text_from_logs([log], REWRITE_HEADER)
    )
    # if log new as below
    condition = ("late" if late else "new") if new else "duplicated"
    # if log not new, then ask again
    # send primary call backs.
    id = update.message.from_user.id
    reply_markdown(update, context, reply_message)
    reply_message += REWRITE_FOOTER
    return {"message": reply_message, "condition": condition, "id": id}


@log_info()
def add_optional_status(update, context):
    # update log optional_status

    session = context.user_data.get("session")
    # save data
    optional_status = update.message.text
    put_sub_category(context.user_data["log_id"], optional_status)
    text_message = ASK_LOCATION_TEXT
    return {"message": text_message}


@log_info()
def add_location(update, context):
    """ add location and ask confirmation """
    # Update longitude and latitude on log table
    # Create confirmation address
    set_location_not_available(update, context)
    success = set_location(update, context)
    # error happened, abort

    # add log text
    log = get_log_by_id(context.user_data.get("log_id"))
    text_message = ASK_LOG_CONFIRMATION_TEXT
    text_message = make_text_from_logs(
        [
            log,
        ],
        text_message,
    )
    condition = "content" if log.status == "signing out" and log.optional_status == "Home" else "done"
    condition = "lunch" if log.status == "getting back" else condition
    return {"condition": condition, "message": text_message}


@log_info()
def confirm_log(update, context):
    """ """
    # update confirmation on log table
    clear_session(update, context)
    return {"message": "Confirmed."}


@log_info()
def check_rewrite_log(update, context):
    log = get_log_by_id(context.user_data.get("log_id"))
    header_message = ASK_REMOVAL_CONFIRMATION.format(log_id=log.id)
    text_message = make_text_from_logs((log,), header_message)
    # add current log data
    return {"message": text_message}


@log_info()
def rewrite_log(update, context):
    log_id = context.user_data.get("log_id")
    session = context.user_data.get("session")
    log = get_log_by_id(log_id)
    member = log.member_fk
    log.delete()
    log = save_log(member, update.message.date, session)
    context.user_data["log_id"] = log.id

    # add info
    text = "You have relogged as below.\n"
    text_message = make_text_from_logs((log,), text)
    text_message += "Please choose where you work."
    return {"message": text_message}


@log_info()
def ask_reason(update, context):
    text = "Please text me the reason."
    return {"message": text}


@log_info()
def receive_reason(update, context):
    text = update.message.text
    log = get_log_by_id(context.user_data.get("log_id"))
    remarks_text = (log.remarks + "\n") if log.remarks else ""
    log.remarks = f"(late) {remarks_text}{text}"
    log.save()
    text_message = "I got your message as below.\n\n"
    text_message += text
    text_message += "\n\nPlease choose where you work."

    return {"message": text_message}


@log_info()
def ask_content(update, context):
    text = "Please text me the today's work."
    return {"message": text}


@log_info()
def confirm_content(update, context):
    answer = update.message.text
    context.user_data["work_content"] = answer
    answer = context.user_data.get("work_content")
    text_message = CHECK_CONTENT_TEXT.format(answer=answer)
    return {"message": text_message}


@log_info()
def save_content(update,  context):
    content = context.user_data.get("work_content")
    post_work_content(update, context, content)
    text = "Content has been saved\n"
    text += "Do you confirm the log?"
    return {"message": text}


def check_distance(log_in, log_out):
    if log_out and log_in:
        x1, y1 = log_out.latitude, log_out.longitude
        x2, y2 = log_in.latitude, log_in.longitude
        if x1 == "Not Available" or x2 == "Not Available":
            return False
        
        p1 = list(map(float, (x1, y1)))
        p2 = list(map(float, (x2, y2)))
        distance = get_distance(p1, p2)
        return True if distance > 0.003 else False
    return False


def get_distance(p1, p2):
    distance = sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    return distance


@log_info()
def check_location(update, context):
    session = context.user_data.get("session")
    log_in, log_out = None, None
    text_message = "Confirmed"
    if session == "signing out":
        # set variable
        member = get_or_register_user(update.message.chat, update.message.from_user)
        log_out = get_or_none_log_of_date(member, update.message.date.date(), "signing out")
        log_in = get_or_none_log_of_date(
            member, update.message.date.date(), "signing in"
        )
        if not log_in:
            text_message = "No sign in information found today.\n"
            text_message = "Please contact the director."
            return {"message": text_message, "condition": "confirmed"}
        if check_distance(log_in, log_out):
            text_message = "Your sign out location is not matched with sign in location.\n"
            text_message += "Please, send us your location again or explain me the diffrence."
            return {"message": text_message, "condition": "location"}
    # update confirmation on log table
    clear_session(update, context)
    return {"message": text_message, "condition": "confirmed"}


def explain_location(update, context):
    return {"message": "Please text me the reason"}

def save_explain(update, context):
    text = update.message.text
    log = get_log_by_id(context.user_data.get("log_id"))
    confirmation_text = (log.confirmation + "\n") if log.confirmation else ""
    log.confirmation = f"(location) {confirmation_text} {text}"
    log.save()
    text_message = "I got your message as below.\n\n"
    text_message += confirmation_text
    text_message += "\n\nIf you want to change it,\nplease press 'Explain The location difference' button"
    return {"message": text_message}