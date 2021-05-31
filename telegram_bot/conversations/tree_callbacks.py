def create_log(update, context):
    pass
    return 0, "Where do you work?"


def add_optional_status(update, context):
    # update log optional_status
    return 0, "Ask location"


def add_location(update, context):
    """ add location and ask confirmation """
    # Update longitude and latitude on log table
    # Create confirmation address
    return 0, "Do you confirm it?"


def confirm_log(update, context):
    """ """
    # update confirmation on log table

    return 0, "Confirmed."