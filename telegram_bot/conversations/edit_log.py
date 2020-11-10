from telegram.ext import ConversationHandler
from features.data_IO import make_text_from_logs, get_logs_by_user_id, get_record_by_log_id, edit_history
from features.log import log_info
from features.message import reply_markdown, set_context
from features.constant import LOG_COLUMN

# Delete log
ANSWER_LOG_ID, ANSWER_CONFIRMATION = map(chr, range(7, 9))


@log_info()
def ask_log_id_to_edit(update, context):
    """ """

    user = update.message.from_user

    rows = get_logs_by_user_id(user.id, 3)
    
    text_message = "Which log do you want to edit?\nPlease send me the log number."
    if rows:
        text_message = make_text_from_logs(rows, text_message)

    reply_markdown(update, context, text_message)

    context.user_data["status"] = "EDIT_LOG_ID"

    return ANSWER_LOG_ID


@log_info()
def ask_confirmation_of_edit(update, context):
    log_id = update.message.text
    try:
        int(log_id)
        keyboard = [["YES", "NO"]]

        log = get_record_by_log_id(log_id)
        logs = (log,)

        header_message = f"Do you really want to do edit log No.{log_id}?\n"
        text_message = make_text_from_logs(logs, header_message)
        reply_markdown(update, context, text_message, keyboard)
    
        chat_id = log.member_fk.id
        print(chat_id)

        set_context(update, context, {"log_id": log_id, "chat_id": chat_id})

        return ANSWER_CONFIRMATION
    except ValueError:
        text_message = "Please. Send me numbers only."
        reply_markdown(update, context, text_message)
        return ANSWER_LOG_ID


@log_info()
def start_edit(update, context):
    choices = {"YES": True, "NO": False}
    answer = choices.get(update.message.text)
    if answer:
        log_id = context.user_data.get("log_id")
        status, history = edit_history(log_id)

        keyboard_dict = {
            "signing in": [
                ["Office", "Home"],
            ],
            "signing out": [
                [
                    "I worked at Office",
                    "I would like to report because I worked at home",
                ]
            ],
            "getting back": [
                ["Without any member of KOICA", "With KOICA Colleagues"],
            ],
        }
        status_dict = {
            "signing in": "SIGN_IN",
            "signing out": "SIGN_OUT",
            "getting back": "GET_BACK",
        }
        context.user_data["status"] = status_dict.get(status)

        text_message = f"start to edit Log No.{log_id} by press button\n"
        reply_markdown(update, context, text_message, keyboard_dict.get(status))
    else:
        text_message = "process has been stoped. The log has not been deleted."
        reply_markdown(update, context, text_message)
        context.user_data.clear()
    return ConversationHandler.END
