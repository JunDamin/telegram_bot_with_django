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

    ret_data = (False, None)
    query = update.callback_query
    (action, data) = separate_callback_data(query.data)


def create_leave_form(
    flow, start_date: datetime.datetime, end_date: datetime.datetime
) -> InlineKeyboardMarkup:

    date_one = start_date.isoformat() if start_date else "Start Date"
    date_two = end_date.isoformat() if end_date else "End Date"

    start_date = start_date if start_date else datetime.date.today()
    end_date = end_date if end_date else datetime.date.today()

    keyboard = []
    first_row = []
    first_row.append(
        InlineKeyboardButton(
            text=date_one,
            callback_data=create_callback_data(
                "DATEPICK",
                (start_date.year, start_date.month, start_date.day),
            ),
        )
    )
    first_row.append(
        InlineKeyboardButton(
            text=date_two,
            callback_data=create_callback_data(
                "DATEPICK",
                (end_date.year, end_date.month, end_date.day),
            ),
        )
    )
    keyboard.append(first_row)

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
                text="End date should be later than start date", callback_data="None"
            )
        )
    else:
        second_row.append(InlineKeyboardButton(text=" ", callback_data=" "))
    if second_row:
        keyboard.append(second_row)

    return InlineKeyboardMarkup(keyboard)
