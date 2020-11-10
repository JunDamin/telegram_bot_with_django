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
ASK_LOCATION = """I see! Please send me your location by click the button on your phone.
  1. Please check your location service is on.(if not please turn on your location service)
  2. Desktop app can not send location"""

ASK_LOG_CONFIRMATION = "You have signed in as below. Do you want to confirm?"