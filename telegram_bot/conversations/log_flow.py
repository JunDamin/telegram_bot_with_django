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
    initiate_private_conversation
)

# set status
(
    ASK_OPTIONAL_STATUS,
    ASK_LOCATION,
    ASK_LOG_CONFIRMATION,
    ASK_CONTENT,
    ASK_CONTENT_CONFIRMATION,
    ASK_OVERWRITE,
    ASK_OVERWRITE_CONFIRMATION,
) = ["log" + str(i) for i in range(7)]


@log_info()
def reply_initiation(update, context):
    # set variable
    chat = update.message.chat
    user = update.message.from_user

    # check chat and user
    register_office(chat)
    member = get_or_register_user(chat, user)

    # set session and log
    status = set_session(update, context)

    log = get_or_none_log_of_date(member, update.message.date.date(), status)
    is_new = False if log else True
    if is_new:
        log = save_log(member, update.message.date, status)
    context.user_data["log_id"] = log.id

    # make text by session
    text = init_group_message.get(status)
    reply_message = (
        text.format(
            first_name=user.first_name, log_id=log.id, report_time=log.local_time()
        )
        if is_new
        else make_text_from_logs([log], REWRITE_HEADER)
    )

    reply_markdown(
        update,
        context,
        reply_message,
    )
    return (
        ask_optional_status(update, context)
        if is_new
        else ask_overwrite(update, context)
    )


def cancel(update, context):
    clear_session(update, context)
    reply_markdown(update, context, "Bye!")
    return -1


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


@log_info()
def ask_overwrite(update, context):
    log = get_log_by_id(context.user_data.get("log_id"))
    send_markdown(
        update,
        context,
        log.member_fk.id,
        make_text_from_logs(
            [
                log,
            ],
            REWRITE_HEADER,
            REWRITE_FOOTER,
        ),
        reply_keyboard.get("overwrite"),
    )
    return ASK_OVERWRITE


def receive_overwrite(update, context):
    is_yes = update.message.text == yes_dict.get("overwrite")
    return (
        ask_overwrite_confirmation(update, context)
        if is_yes
        else cancel(update, context)
    )


@log_info()
def ask_overwrite_confirmation(update, context):
    log = get_log_by_id(context.user_data.get("log_id"))
    header_message = ASK_REMOVAL_CONFIRMATION.format(log_id=log.id)
    text_message = make_text_from_logs((log,), header_message)
    reply_markdown(
        update, context, text_message, reply_keyboard.get("overwrite_confirmation")
    )
    return ASK_OVERWRITE_CONFIRMATION


def receive_overwrite_confirmation(update, context):
    log_id = context.user_data.get("log_id")
    session = context.user_data.get("session")
    is_yes = update.message.text == yes_dict.get("overwrite_confirmation")
    if not is_yes:
        return cancel(update, context)
    log = get_log_by_id(log_id)
    member = log.member_fk
    log.delete()
    text_message = INFO_REMOVAL.format(log_id=log_id)
    reply_markdown(update, context, text_message)
    log = save_log(member, update.message.date, session)
    context.user_data["log_id"] = log.id
    return ask_optional_status(update, context)


@log_info()
def ask_optional_status(update, context):
    session = context.user_data.get("session")
    log = get_log_by_id(context.user_data.get("log_id"))

    if not (session or log):
        return cancel(update, context)
    if hasattr(log, "work_content"):
        log.work_content.delete()

    text_message = optional_status_message.get(session)
    keyboard = optional_status_keyboard.get(session)
    initiate_private_conversation(
        update,
        context,
        log.member_fk.id,
        text_message.format(
            first_name=log.member_fk.first_name,
            log_id=log.id,
            report_time=log.local_time(),
        ),
        keyboard,
    )
    return ASK_OPTIONAL_STATUS


def receive_optional_status(update, context):
    session = context.user_data.get("session")
    optional_status = update.message.text
    if session == "siging out":
        check_branch = {
            "I worked at Office": "Office",
            "YES": "Home",
        }
        optional_status = check_branch.get(optional_status)
    put_sub_category(context.user_data["log_id"], optional_status)
    if (
        session == "signing out"
        and update.message.text == "I worked at home(I summit daily report)"
    ):
        return ask_content(update, context)

    return ask_location(update, context)


@log_info()
def ask_location(update, context):
    text_message = ASK_LOCATION_TEXT
    keyboard = ASK_LOCATION_KEYBOARD
    reply_markdown(update, context, text_message, keyboard)
    return ASK_LOCATION


def receive_location(update, context):
    set_location_not_available(update, context)
    success = set_location(update, context)
    return ask_log_confirmation(update, context) if success else cancel(update, context)


@log_info()
def ask_log_confirmation(update, context):
    log = get_log_by_id(context.user_data.get("log_id"))
    HEADER_MESSAGE = ASK_LOG_CONFIRMATION_TEXT
    text_message = HEADER_MESSAGE
    keyboard = ASK_LOG_CONFIRMATION_KEYBOARD
    text_message = make_text_from_logs(
        [
            log,
        ],
        text_message,
    )

    reply_markdown(update, context, text_message, keyboard)
    return ASK_LOG_CONFIRMATION


def receive_log_confirmation(update, context):
    choices = {"Confirm": True, "Edit": False}
    answer = choices.get(update.message.text)

    check_distance(update, context)

    if answer:
        put_confirmation(update, context)
        context.user_data.clear()
        text_message = "Confirmed"
        reply_markdown(update, context, text_message)
        return -1
    else:
        return ask_optional_status(update, context)


def check_distance(update, context):
    session = context.user_data.get("session")

    if session == "signing out":
        # set variable
        member = get_or_register_user(update.message.chat, update.message.from_user)

        log_out = get_or_none_log_of_date(member, update.message.date.date(), session)
        log_in = get_or_none_log_of_date(member, update.message.date.date(), "signing in")

        if log_out and log_in:
            x1, y1 = log_out.longitude, log_out.latitude
            x2, y2 = log_in.longitude, log_in.latitude

            if x1 == "Not Available" or x2 == "Not Available":
                output = "Not Available"
            else:
                x1, y1 = map(float, (x1, y1))
                x2, y2 = map(float, (x2, y2))
                distance = sqrt((x1-x2)**2 + (y1-y2)**2)
                if distance < 0.003:
                    output = "OK"
                else:
                    output = "Need to Check"
            log_out.distance = output

        if not log_in:
            log_out.distance = "No Log in"

        log_out.save()


@log_info()
def ask_content(update, context):
    text_message = ASK_WORK_CONTENT
    reply_markdown(update, context, text_message)
    return ASK_CONTENT


def receive_content(update, context):
    answer = update.message.text
    context.user_data["work_content"] = answer
    return ask_content_confirmation(update, context)


@log_info()
def ask_content_confirmation(update, context):
    answer = context.user_data.get("work_content")
    text_message = CHECK_CONTENT_TEXT.format(answer=answer)
    keyboard = CHECK_CONTENT_KEYBOARD
    reply_markdown(update, context, text_message, keyboard)
            
    return ASK_CONTENT_CONFIRMATION


def receive_content_confirmation(update, context):
    content = context.user_data.get("work_content")
    post_work_content(update, context, content)

    return ask_location(update, context)
