SIGN_IN_GREETING = (
        """Good morning, `{first_name}`.\nYou have signed in with Log No.{log_id}"""
    )
SIGN_TIME = """signing time: {report_time}"""
CHECK_DM = """_Please check my DM(Direct Message) to you"""
ASK_SIGN_IN_INFO = """Would you like to share where you work?"""

SIGN_IN_GROUP_MESSAGE = "\n".join([SIGN_IN_GREETING, CHECK_DM, SIGN_TIME])
SIGN_IN_PRIVATE_MESSAGE = "\n".join([SIGN_IN_GREETING, ASK_SIGN_IN_INFO, SIGN_TIME])


REWRITE_HEADER = "You have already logged as below. "
REWRITE_FOOTER = "\nDo you want to *_delete it_* and log it again? or SKIP it?"