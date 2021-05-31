def cancel(update, context):
    return {"message": "OK. Good bye!"}


def create_log(update, context):
    # if log new as below
    text = "Where do you work?"
    condition = "duplicated"
    # if log not new, then ask again
    return {"message": text, "condition": condition}


def add_optional_status(update, context):
    # update log optional_status
    return {"message": "Please share your location."}


def add_location(update, context):
    """ add location and ask confirmation """
    # Update longitude and latitude on log table
    # Create confirmation address
    text = "Here is your log. \n"
    # add log text
    text += "Do you confirm it?"

    return {"message": text}


def confirm_log(update, context):
    """ """
    # update confirmation on log table
    return {"message": "Confirmed."}


def check_rewrite_log(update, context):
    text = "Here is your log of today.\n"
    # add current log data
    text += "Do you really rewrite the log?"
    return {"message": text}


def rewrite_log(update, context):
    text = "You have relogged as below.\n"
    # add info
    text += "Please choose where you work."
    return {"message": text}