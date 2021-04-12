"""
Base methods for calendar keyboard creation and processing
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import date, timedelta
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
    today = date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month
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
                        callback_data=create_callback_data("DAY", (year, month, day)),
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


def process_half_day_off(update, context):
    """getting input annual leave"""
    query = update.callback_query
    (action, data) = separate_callback_data(query.data)
    year, month, day, curr = get_days(update, context)

    if action == "MORNING":
        context.user_data["off_type"] = "Morning"
        query.edit_message_text(
            text="Select Date for morning day off",
            reply_markup=create_calendar(year, month),
        )
    elif action == "AFTERNOON":
        context.user_data["off_type"] = "Afternoon"
        query.edit_message_text(
            text="Select Date for morning day off",
            reply_markup=create_calendar(year, month),
        )

    ret_data = handle_cal_callback(update, context)

    update.callback_query.answer()
    return ret_data


def handle_cal_callback(update, context):
    query = update.callback_query
    (action, data) = separate_callback_data(query.data)
    year, month, day, curr = get_days(update, context)
    ret_data = (False, None)

    print(action)
    if action == "IGNORE":
        update.answer_callback_query(callback_query_id=query.id)
    elif action == "DAY":
        context.user_data["date"] = date(year, month, day).isoformat()
        ret_data = True, date(year, month, day)
    elif action == "PREV":
        pre = curr - timedelta(days=1)
        query.edit_message_text(
            text=query.message.text,
            reply_markup=create_calendar(int(pre.year), int(pre.month)),
        )
    elif action == "NEXT":
        ne = curr + timedelta(days=31)
        query.edit_message_text(
            text=query.message.text,
            reply_markup=create_calendar(int(ne.year), int(ne.month)),
        )
    else:
        # query.edit_message_text(text="Something went wrong!")
        pass
    return ret_data


def get_days(update, context):
    query = update.callback_query
    (action, data) = separate_callback_data(query.data)
    if data and len(data) == 3:
        year, month, day = data
    else:
        today = date.today()
        year, month, day = today.year, today.month, today.day
    curr = date(int(year), int(month), 1)
    year, month, day = map(int, (year, month, day))

    return year, month, day, curr


def create_half_day_options(update, context):
    user_data = context.user_data

    off_type = user_data.get("off_type")
    date = user_data.get("date")
    print(off_type, date)
    if off_type and date:
        text = f"You choose {off_type} off on {date}"
        text += "\nIf it is correct, please press confirm button."
    else:
        text = "please select the type"

    keyboard = [
        [
            InlineKeyboardButton(
                text="Morning", callback_data=create_callback_data("MORNING")
            ),
            InlineKeyboardButton(
                text="Afternoon", callback_data=create_callback_data("AFTERNOON")
            ),
        ],
        [
            InlineKeyboardButton(
                text="Cancel", callback_data=create_callback_data("CANCEL")
            )
        ],
    ]

    if off_type and date:
        keyboard[1].append(
            InlineKeyboardButton(
                text="Confirm", callback_data=create_callback_data("CONFIRM")
            )
        )

    return text, InlineKeyboardMarkup(keyboard)


def create_full_day_options(update, context):
    user_data = context.user_data

    start_date = user_data.get("Start date")
    end_date = user_data.get("End date")
    date_i = start_date if start_date else "Start Date"
    date_f = end_date if end_date else "End Date"

    print("checK", start_date and end_date, start_date, end_date)
    if start_date and end_date:
        text = f"You choose {date_i} off on {date_f}"
        text += "\nIf it is correct, please press confirm button."
    else:
        text = "Please choose the dates"

    keyboard = [
        [
            InlineKeyboardButton(
                text=date_i, callback_data=create_callback_data("START_DATE")
            ),
            InlineKeyboardButton(
                text=date_f, callback_data=create_callback_data("END_DATE")
            ),
        ],
        [
            InlineKeyboardButton(
                text="Cancel", callback_data=create_callback_data("CANCEL")
            )
        ],
    ]

    if start_date and end_date:
        keyboard[1].append(
            InlineKeyboardButton(
                text="Confirm", callback_data=create_callback_data("CONFIRM")
            )
        )
    return text, InlineKeyboardMarkup(keyboard)


def process_full_day_off(update, context):
    """getting input annual leave"""
    query = update.callback_query
    (action, data) = separate_callback_data(query.data)
    year, month, day, curr = get_days(update, context)

    print(context.user_data)

    if action == "DAY":
        date_type = context.user_data["date_type"]
        context.user_data[date_type] = context.user_data.get("date")

    if action == "START_DATE":
        context.user_data["date_type"] = "Start date"
        query.edit_message_text(
            text="Select start date of annual leave",
            reply_markup=create_calendar(year, month),
        )
    elif action == "END_DATE":
        context.user_data["date_type"] = "End date"
        query.edit_message_text(
            text="Select end date of annual leave",
            reply_markup=create_calendar(year, month),
        )

    ret_data = handle_cal_callback(update, context)
    date_type = context.user_data.get("date_type")

    if ret_data[0]:
        context.user_data[date_type] = ret_data[1].isoformat()
    update.callback_query.answer()

    print(context.user_data)

    return ret_data
