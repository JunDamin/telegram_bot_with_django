from telegram import KeyboardButton

SIGN_IN_GREETING = (
    """Good morning, `{first_name}`.\nYou have signed in with Log No.{log_id}"""
)
SIGN_TIME = """signing time: {report_time}"""
CHECK_DM = """Please check my DM(Direct Message) to you"""
ASK_SIGN_IN_INFO = """Would you like to share where you work?"""

SIGN_IN_GROUP_MESSAGE = "\n".join([SIGN_IN_GREETING, CHECK_DM, SIGN_TIME])
SIGN_IN_PRIVATE_MESSAGE = "\n".join([SIGN_IN_GREETING, ASK_SIGN_IN_INFO, SIGN_TIME])


REWRITE_HEADER = "You have already logged as below. "
REWRITE_FOOTER = "\nDo you want to *_delete it_* and log it again? or SKIP it?"

ASK_REMOVAL_CONFIRMATION = "Do you really want to do remove log No.{log_id}?\n"
INFO_REMOVAL = "Log No. {log_id} has been Deleted\n"
STOP_REMOVAL = "process has been stoped. The log has not been deleted."

ERROR_MESSAGE = "An Error has been made. Please try again."

ASK_SIGN_IN_OPTIONAL_STATUS = "Would you like to share where you work?"

ASK_SIGN_IN_CONFIRMATION = "You have signed in as below. Do you want to confirm?"

SIGN_OUT_GREETING = (
    """Good evening, {first_name}.\nYou have signed out today with Log No.{log_id}"""
)
ASK_SIGN_OUT_INFO = "Would you like to share your today's content of work?"
CHECK_DM = """"Please check my DM(Direct Message) to you"""

SIGN_OUT_GROUP_MESSAGE = "\n".join([SIGN_OUT_GREETING, CHECK_DM, SIGN_TIME])
SIGN_OUT_PRIVATE_MESSAGE = "\n".join([SIGN_OUT_GREETING, ASK_SIGN_OUT_INFO, SIGN_TIME])

ASK_SIGN_OUT_CONFIRMATION = "You have signed out as below. Do you want to confirm?"

ASK_WORK_TYPE = "Would you like to share your today's content of work?"

GET_BACK_GREETING = """Good afternoon, {first_name}.\n
Welcome back. You have been logged with Log No.{log_id}"""
ASK_GET_BACK_INFO = """Did you have lunch with KOICA collagues?"""
GET_BACK_GROUP_MESSAGE = "\n".join([GET_BACK_GREETING, CHECK_DM, SIGN_TIME])
GET_BACK_PRIVATE_MESSAGE = "\n".join([GET_BACK_GREETING, ASK_GET_BACK_INFO, SIGN_TIME])

ASK_GET_BACK_CONFIRMATION = "You have gotten back as below. Do you want to confirm?"

init_group_message = {
    "signing in": SIGN_IN_GROUP_MESSAGE,
    "signing out": SIGN_OUT_GROUP_MESSAGE,
    "getting back": GET_BACK_GROUP_MESSAGE,
}


# REGEX and keyboard
start_regex = {
    "signing in": "sign.{0,3} in.?$",
    "signing out": "sign.{0,3} out.?$",
    "getting back": "back from break.?$|back to work.?$|lunch over.?$|break over.?$",
}

yes_dict = {
    "overwrite": "Delete and Rewrite",
    "overwrite_confirmation": "Remove the log",
}

reply_keyboard = {
    "overwrite": [
        [yes_dict.get("overwrite"), "SKIP"],
    ],
    "overwrite_confirmation": [
        [yes_dict.get("overwrite_confirmation"), "NO"],
    ],
}

ask_overwrite_regex = [yes_dict.get("overwrite"), "SKIP"]
ask_overwrite_confirmation_regex = [yes_dict.get("overwrite_confirmation"), "NO"]


optional_status_message = {
    "signing in": SIGN_IN_PRIVATE_MESSAGE,
    "signing out": SIGN_OUT_PRIVATE_MESSAGE,
    "getting back": GET_BACK_PRIVATE_MESSAGE,
}

optional_status_keyboard = {
    "signing in": [
        ["Office", "Home", "Business Trip"],
    ],
    "signing out": [
        [
            "I worked at Office",
            "I worked at home(I submit daily report)",
        ]
    ],
    "getting back": [
        ["Without any member of KOICA", "With KOICA Colleagues"],
    ],
}
optional_status_regex = []
for i in optional_status_keyboard.values():
    optional_status_regex.extend(*i)

optional_status_regex = map(lambda x: x.replace("(", "\\("), optional_status_regex)
optional_status_regex = map(lambda x: x.replace(")", "\\)"), optional_status_regex)
optional_status_regex = list(optional_status_regex)

ASK_LOCATION_TEXT = """I see! Please send me your location by click the button on your phone.
  1. Please check your location service is on.(if not please turn on your location service)
  2. Desktop app can not send location"""


ASK_LOCATION_KEYBOARD = [
    [KeyboardButton("Share Location", request_location=True), "Not Available"],
]


ASK_LOG_CONFIRMATION_TEXT = "You have logged as below. Do you want to confirm?"
ASK_LOG_CONFIRMATION_KEYBOARD = [["Confirm", "Edit"]]

ask_log_confirmation_regex = []
for i in ASK_LOG_CONFIRMATION_KEYBOARD:
    ask_log_confirmation_regex.extend(i)


ASK_WORK_CONTENT = "OK. Please text me what you have done today for work briefly."
CHECK_CONTENT = "Content of Work\n{answer}\n\nIs it ok?"

CHECK_CONTENT_TEXT = "Content of Work\n{answer}\n\nIs it ok?"
CHECK_CONTENT_KEYBOARD = [["YES", "NO"]]

ask_conetent_confirmation_regex = []

for i in CHECK_CONTENT_KEYBOARD:
    ask_conetent_confirmation_regex.extend(i)
