from telegram.ext import ConversationHandler
from features.data_IO import (
    get_text_of_log_by_id,
    get_log_by_id,
    put_remarks_by_id,
)
from features.message import reply_markdown
from features.log import log_info
from conversations.tree_classes import (
    Node,
    ConversationTree,
)


@log_info()
def ask_log_id_for_remarks(update, context):
    text_message = """Which log do you want to add remarks?\nPlease send me the log number. """
    context.user_data["status"] = "ASK_REMARKS_CONTENT"
    return {"message": text_message, "keyboard": [[]]}


@log_info()
def ask_content_for_remarks(update, context):
    log_id = update.message.text
    try:
        record = get_log_by_id(log_id)
        if record:
            context.user_data["remarks_log_id"] = log_id
            text_message = "What remarks? do you want to add?\n"
            text_message += get_text_of_log_by_id(log_id)
            return {"message": text_message}
        else:
            raise ValueError
    except ValueError:
        text_message = "log id is not exist. Please try from the beginning."
        return {"message": text_message, "path": "escape"}


@log_info()
def set_remarks(update, context):
    log_id = context.user_data.get("remarks_log_id")
    content = update.message.text
    put_remarks_by_id(content, log_id)
    text_message = "remarks has been updated as below.\n"
    text_message += get_text_of_log_by_id(log_id)
    context.user_data.clear()
    return {"message": text_message}


starting = Node("start add remarks", "/비고작성", ask_log_id_for_remarks, isEntry=True)
get_log_id = Node("get log id", "[0-9]*", ask_content_for_remarks).set_parents(
    [starting]
)
putting_remarks = Node(
    "save remarks", "text", set_remarks, inputType="text"
).set_parents([get_log_id])

remarks_tree = ConversationTree(starting)