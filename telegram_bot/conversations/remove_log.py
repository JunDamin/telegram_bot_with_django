from features.data_IO import (
    make_text_from_logs,
    get_record_by_log_id,
    delete_log_and_content,
)
from features.log import log_info
from features.message import (
    reply_markdown,
)
from conversations.tree_classes import (
    Node,
    ConversationTree,
)


@log_info()
def ask_log_id_to_remove(update, context):
    """ """
    text_message = "Which log do you want to remove?\nPlease send me the log number."
    context.user_data["status"] = "REMOVE_LOG_ID"
    return {"message": text_message, "keyboard": [[]]}


@log_info()
def ask_confirmation_of_removal(update, context):
    log_id = update.message.text
    try:
        int(log_id)
        context.user_data["remove_log_id"] = log_id
        row = get_record_by_log_id(log_id)
        if not row:
            raise ValueError
        rows = (row,)
        header_message = f"Do you really want to do remove log No.{log_id}?\n"
        text_message = make_text_from_logs(rows, header_message)
        return {"message": text_message}

    except ValueError:
        text_message = "Please. Send me numbers only."
        return {"message": text_message, "path": "redo"}


def answer_yes(update, context):
    log_id = context.user_data.get("remove_log_id")
    delete_log_and_content(update, context, log_id)
    text_message = f"Log No.{log_id} has been Deleted\n"
    context.user_data.clear()
    return {"message": text_message}


def answer_no(update, context):
    text_message = "process has been stoped. The log has not been deleted."
    return {"message": text_message}


starting = Node("Delete log", "/로그삭제", ask_log_id_to_remove, isEntry=True)
checking_log = Node("Check log", "[0-9]*", ask_confirmation_of_removal).set_parents(
    [starting]
)
yes = Node("Yes", "YES", answer_yes).set_parents([checking_log])
no = Node("No", "NO", answer_no).set_parents([checking_log])

remove_tree = ConversationTree(starting)