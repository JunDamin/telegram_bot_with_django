from features.data_IO import make_text_from_logs, get_logs_by_user_id, get_record_by_log_id, edit_history
from features.log import log_info
from features.message import set_context
from conversations.tree_classes import (
    Node,
    ConversationTree,
)


@log_info()
def ask_log_id_to_edit(update, context):
    """ """

    user = update.message.from_user
    rows = get_logs_by_user_id(user.id, 3)
    text_message = "Which log do you want to edit?\nPlease send me the log number."
    if rows:
        text_message = make_text_from_logs(rows, text_message)
    context.user_data["status"] = "EDIT_LOG_ID"

    return {"message": text_message, "keyboard": [[]]}


@log_info()
def ask_confirmation_of_edit(update, context):
    log_id = update.message.text
    try:
        log = get_record_by_log_id(log_id)
        print(log)
        logs = (log,)
        if not log:
            raise ValueError
        header_message = f"Do you really want to do edit log No.{log_id}?\n"
        text_message = make_text_from_logs(logs, header_message)
        chat_id = log.member_fk.id
        set_context(update, context, {"log_id": log_id, "chat_id": chat_id})
        return {"message": text_message}
    except ValueError:
        text_message = "Log ID is not exist. Please text me the log ID"
        return {"message": text_message, "path": "redo", "keyboard": [[]]}


def answer_yes(update, context):
    log_id = context.user_data.get("log_id")
    status, history = edit_history(log_id)

    keyboard_dict = {
        "signing in": [
            ["Office", "Home"],
        ],
        "signing out": [
            ["Office", "Home"],
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
    keyboard = keyboard_dict[status]
    return {"message": text_message, "keyboard": keyboard}


def answer_no(update, context):
    text_message = "process has been stoped. Please try again."
    context.user_data.clear()
    return {"message": text_message}


starting = Node("start editing", "edit", ask_log_id_to_edit, isEntry=True, inputType="command")
rechecking = Node("checking id", "[0-9,\s]*", ask_confirmation_of_edit).set_parents([starting])
yes = Node("Yes", "YES", answer_yes).set_parents([rechecking])
no = Node("No", "NO", answer_no).set_parents([rechecking])

edit_tree = ConversationTree(starting)