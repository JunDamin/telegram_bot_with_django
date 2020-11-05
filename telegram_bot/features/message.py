from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.error import Unauthorized
from features.data_IO import (
    get_today_log_of_chat_id_category,
    post_basic_user_data,
    put_location,
)


def split_text_with_chunk_size_by_line(text_message, chunk_size=4096):
    # telegram api length limit is 4096
    text_lines = text_message.splitlines()
    text_list = []
    temp_text = ""
    for line in text_lines:
        joined_text = "\n".join([temp_text, line])
        if len(joined_text) < chunk_size:
            temp_text = joined_text
        else:
            text_list.append(temp_text)
            temp_text = line
    text_list.append(temp_text)
    return text_list


def send_markdown(update, context, user_id, text_message, reply_keyboard=False):

    text_message = convert_text_to_md(text_message)
    text_list = split_text_with_chunk_size_by_line(text_message)

    for text in text_list:
        context.bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            if reply_keyboard
            else ReplyKeyboardRemove(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )


def reply_markdown(update, context, text_message, reply_keyboard=False):

    text_message = convert_text_to_md(text_message)
    text_list = split_text_with_chunk_size_by_line(text_message)

    for text in text_list:
        update.message.reply_markdown_v2(
            text=text,
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            if reply_keyboard
            else ReplyKeyboardRemove(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )


def convert_text_to_md(text):
    convert_dict = {
        ".": "\\.",
        "-": "\\-",
        "!": "\\!",
        "(": "\\(",
        ")": "\\)",
        "+": "\\+",
        "=": "\\=",
    }
    for key in convert_dict:
        text = text.replace(key, convert_dict[key])

    return text


def initiate_private_conversation(
    update, context, group_message, private_message, keyboard
):
    user = update.message.from_user
    group_keyboard = [["Sign In", "Back to Work", "Sign Out"]]
    try:
        # send to group chat
        send_markdown(update, context, update.message.chat.id, group_message)
        send_markdown(update, context, user.id, private_message, keyboard)

    except Unauthorized:
        text_message = "Please, send 'Hi!' to me as DM(Direct Message) to authorize!"
        reply_markdown(update, context, text_message, group_keyboard)


def get_log_id_and_record(update, context, session: str):
    user = update.message.from_user
    rows = get_today_log_of_chat_id_category(user.id, session)
    if rows:
        record = rows[0]
        log_id = record[0]
        is_exist = True
    else:
        log_id = post_basic_user_data(update, context, session)
        (record,) = get_today_log_of_chat_id_category(user.id, session)
        is_exist = False
    return log_id, record, is_exist


def set_context(update, context, context_dict):
    for key in context_dict:
        context.user_data[key] = context_dict[key]
    return None


def set_location(update, context):
    user_location = update.message.location
    user_data = context.user_data
    if put_location(user_location, user_data):
        return 1
    else:
        text_message = ("""Something went wrong. Please try again""",)
        reply_markdown(update, context, text_message)
        return 0


def send_initiating_message_by_branch(update, context, is_exist, data_dict: dict):
    """
    docstring
    """
    if not is_exist:
        data = data_dict.get("new")
        # send Private message to update
        initiate_private_conversation(
            update,
            context,
            data["group_message"],
            data["private_message"],
            data["keyboard"],
        )
        return data["return"]
    else:
        data = data_dict.get("rewrite")
        initiate_private_conversation(
            update,
            context,
            data["group_message"],
            data["private_message"],
            data["keyboard"],
        )
        return data["return"]


def set_location_not_available(update, context):
    if update.message.text == "Not Available":
        update.message.location = lambda x: None
        setattr(update.message.location, "longitude", "Not Available")
        setattr(update.message.location, "latitude", "Not Available")
        print("Not Available")
