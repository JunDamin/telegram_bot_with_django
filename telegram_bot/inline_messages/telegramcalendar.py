"""
Base methods for calendar keyboard creation and processing
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import json
import calendar


# callback data shouldn't be longer than 64(?) characters
def create_callback_data(action="IGNORE", data=None):
    """ Create the callback data associated to each button"""
    return f"{action};{json.dumps(data)}"


def separate_callback_data(callback):
    """Separate the callback data"""
    callback = callback.split(";")
    return callback[0], json.loads(callback[1])


def create_calendar(year=None, month=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the corrent year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    data_ignore = create_callback_data("IGNORE", None)
    keyboard = []
    # First row - Month and year
    row = []
    row.append(
        InlineKeyboardButton(
            calendar.month_name[month] + " " + str(year), callback_data=data_ignore
        )
    )
    keyboard.append(row)
    # Second row - week Days
    row = []
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        row.append(InlineKeyboardButton(day, callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
            else:
                row.append(
                    InlineKeyboardButton(
                        str(day),
                        callback_data=create_callback_data(
                            "SELECT_DAY", (year, month, day)
                        ),
                    )
                )
        keyboard.append(row)
    # Last row - Buttons
    row = []
    row.append(
        InlineKeyboardButton(
            "<",
            callback_data=create_callback_data("PREV-MONTH", (year, month, day)),
        )
    )
    row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
    row.append(
        InlineKeyboardButton(
            ">",
            callback_data=create_callback_data("NEXT-MONTH", (year, month, day)),
        )
    )
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_calendar_selection(update, context):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backword is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot : The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean, datetime.datetime), indicating if a date is selected
    and returning the date if so.
    """
    ret_data = (False, None)
    query = update.callback_query
    (action, data) = separate_callback_data(query.data)
    year, month, day = data
    curr = datetime.datetime(int(year), int(month), 1)
    year, month, day = map(int, (year, month, day))
    if action == "IGNORE":
        update.answer_callback_query(callback_query_id=query.id)
    elif action == "SELECT_DAY":
        query.edit_message_text(
            text=datetime.date(year, month, day).isoformat(),
        )
        ret_data = True, datetime.datetime(year, month, day)
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        query.edit_message_text(
            text=query.message.text,
            reply_markup=create_calendar(int(pre.year), int(pre.month)),
        )
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        query.edit_message_text(
            text=query.message.text,
            reply_markup=create_calendar(int(ne.year), int(ne.month)),
        )
    elif action == "DATEPICK":
        query.edit_message_text(
            text="Pick a date",
            reply_markup=create_calendar(),
        )
    else:
        query.edit_message_text(
            callback_query_id=query.id, text="Something went wrong!"
        )
        # UNKNOWN
    update.callback_query.answer()
    return ret_data


def input_annual_leave(update, context):
    """getting input annual leave"""

    query = update.callback_query
    (action, data) = separate_callback_data(query.data)
    year, month, day = data
    curr = datetime.datetime(int(year), int(month), 1)
    year, month, day = map(int, (year, month, day))
    if action == "IGNORE":
        update.answer_callback_query(callback_query_id=query.id)
    elif action == "SELECT_DAY":
        ret_data = True, datetime.datetime(year, month, day)
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        query.edit_message_text(
            text=query.message.text,
            reply_markup=create_calendar(int(pre.year), int(pre.month)),
        )
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        query.edit_message_text(
            text=query.message.text,
            reply_markup=create_calendar(int(ne.year), int(ne.month)),
        )
    else:
        query.edit_message_text(
            callback_query_id=query.id, text="Something went wrong!"
        )
        # UNKNOWN
    update.callback_query.answer()
    return ret_data


def create_leave_form(start_date: str, end_date: str) -> InlineKeyboardMarkup:

    date_one = start_date if start_date else "Start Date"
    date_two = end_date if end_date else "End Date"

    start = (
        datetime.datetime.fromisoformat(start_date)
        if start_date
        else datetime.date.today()
    )
    end = (
        datetime.datetime.fromisoformat(end_date) if end_date else datetime.date.today()
    )

    keyboard = []
    # Set Datepicker
    first_row = []
    first_row.append(
        InlineKeyboardButton(
            text=date_one,
            callback_data=create_callback_data(
                "START_DATE",
                (start.year, start.month, start.day),
            ),
        )
    )
    first_row.append(
        InlineKeyboardButton(
            text=date_two,
            callback_data=create_callback_data(
                "END_DATE",
                (end.year, end.month, end.day),
            ),
        )
    )
    keyboard.append(first_row)

    # check whether date is added
    if not start_date and not end_date:
        return InlineKeyboardMarkup(keyboard)

    second_row = []
    if start_date <= end_date:
        second_row.append(
            InlineKeyboardButton(
                text="Confirm", callback_data=f"CONFIRM;{date_one};{date_two}"
            )
        )
    elif start_date > end_date:
        second_row.append(
            InlineKeyboardButton(
                text="End date should be later than start date",
                callback_data=create_callback_data("IGNORE"),
            )
        )
    else:
        second_row.append(InlineKeyboardButton(text=" ", callback_data=" "))
    if second_row:
        keyboard.append(second_row)

    return InlineKeyboardMarkup(keyboard)
