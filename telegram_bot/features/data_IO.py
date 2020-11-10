import pytz
from datetime import date, timedelta, datetime
from logs.models import Log, WorkContent
from staff.models import Member
from chats.models import Chat
from offices.models import Office
from features.text_function import make_record_text
from features.constant import LOG_COLUMN


def return_row(log):
    return (
        log.id,
        log.member_fk,
        log.first_name,
        log.last_name,
        log.log_datetime,
        log.status,
        log.optional_status,
        log.longitude,
        log.latitude,
        log.remarks,
        log.confirmation,
        "",
    )


def check_status(context, status):
    user_data = context.user_data
    user_status = user_data.get("status")
    return status == user_status


def put_sub_category(log_id, sub_category):
    log = Log.objects.get(id=log_id)
    log.optional_status = sub_category
    log.save()


def post_basic_user_data(update, context, status):
    """
    return: log_id
    """
    _chat = update.message.chat
    _member = update.message.from_user
    log_datetime = update.message.date

    member = get_or_register_user(_chat, _member)

    log = save_log(member, log_datetime, status)

    return log


def register_office(_chat):
    chat = get_or_create_chat(_chat.id, _chat.type, _chat.title)
    chat.office_fk = Office.objects.get(id=1)


def get_or_register_user(_chat, _user):
    chat = Chat.objects.get_or_none(id=_chat.id)
    office = chat.office_fk
    member = get_or_create_member(_user.id, _user.first_name, _user.last_name, office)
    return member


def get_or_create_chat(chat_id, chat_type, chat_name):
    chat = Chat.objects.get_or_none(id=chat_id)
    if not chat:
        chat = Chat(
            id=chat_id,
            chat_type=chat_type,
            chat_name=chat_name,
        )
        chat.save()
    return chat


def get_or_create_member(user_id, first_name, last_name, office):
    """ """
    member = Member.objects.get_or_none(id=str(user_id))
    if not member:
        member = Member(
            id=str(user_id),
            first_name=first_name,
            last_name=last_name,
            office_fk=office,
        )
        member.save()
    return member


def save_log(member, log_datetime, status):
    log = Log(
        member_fk=member,
        log_datetime=log_datetime.astimezone(pytz.timezone("Africa/Douala")),
        status=status,
    )
    log.save()

    return log


def set_user_context(update, context, status):
    user = update.message.from_user

    basic_user_data = {
        "chat_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "timestamp": update.message.date.astimezone(pytz.timezone("Africa/Douala")),
        "category": status,
    }
    for key in basic_user_data:
        context.user_data[key] = basic_user_data[key]


def get_logs_of_today():

    start_date = date.today()
    logs = Log.objects.filter(log_datetime=start_date)
    header_message = f"Today's Logging\n({date.today().isoformat()})"
    rows = map(return_row, logs)
    text_message = make_text_from_logs(rows, header_message)

    return text_message


def get_logs_of_the_day(the_date):

    start_date = date.fromisoformat(the_date)

    logs = Log.objects.filter(log_datetime=start_date)
    header_message = f"Today's Logging\n({date.today().isoformat()})"
    rows = map(return_row, logs)

    header_message = f"{start_date.isoformat()}'s Logging\n"
    text_message = make_text_from_logs(rows, header_message)

    return text_message


def get_today_log_of_chat_id_category(telegram_id, status):
    start_date = date.today()

    member = Member.objects.get_or_none(id=telegram_id)
    if not member:
        return False
    log = Log.objects.get_or_none(
        log_datetime__date=start_date, member_fk=member, status=status
    )

    return log


def get_record_by_log_id(log_id):

    log = Log.objects.get_or_none(id=log_id)
    row = return_row(log) if log else None

    return row


def get_record_by_log_ids(log_ids: str):

    id_list = log_ids.split(",")
    logs = Log.objects.filter(id__in=id_list)
    rows = map(return_row, logs)

    return rows


def get_text_of_log_by_id(log_id):

    log = Log.objects.get_or_none(id=log_id)
    row = return_row(log) if log else None
    rows = (row,)
    text_message = make_text_from_logs(rows)

    return text_message


def get_text_of_log_by_ids(log_ids):

    id_list = log_ids.split(",")
    logs = Log.objects.filter(id__in=id_list)
    rows = map(return_row, logs)

    text_message = make_text_from_logs(rows)

    return text_message


def put_location(location, user_data):
    """
    docstring
    """

    if not location:
        return False

    id = user_data.get("log_id")
    log = Log.objects.get_or_none(id=id)

    if not log:
        return False

    log.longitude = location.longitude
    log.latitude = location.latitude
    log.save()

    return True


def put_confirmation(update, context):
    log = Log.objects.get(id=context.user_data.get("log_id"))
    log.confirmation = "user confirmed"
    log.save()


def post_work_content(update, context, content):

    user = update.message.from_user

    member = Member.objects.get(telegram_id=user.id)
    log = Log.objects.get(id=context.user_data.get("log_id"))

    if hasattr(log, "work_content"):
        work_content = log.work_content
        work_content.content = content
        work_content.member_fk = member
        work_content.first_name = member.first_name
        work_content.last_name = member.last_name
        work_content.log_fk = log
    else:
        work_content = WorkContent(
            member_fk=member,
            first_name=member.first_name,
            last_name=member.last_name,
            content=content,
            log_fk=log,
        )
    work_content.save()


def delete_log_and_content(update, context, log_id=None):
    """"""
    if not log_id:
        log_id = context.user_data.get("log_id")
    log = Log.objects.get(id=log_id)
    log.delete()

    return log_id


def delete_content(update, context):

    log_id = context.user_data.get("log_id")
    log = Log.objects.get(id=log_id)
    work_content = log.work_content.all()
    work_content.delete()
    return log_id


def make_text_from_logs(logs, header="", footer=""):

    text_message = header

    chat_id = ""
    for log in logs:
        user = log.member_fk

        if chat_id != user.id:
            chat_id = user.id
            text_message += f"\n\n*_{user.first_name} {user.last_name}_'s log as below*\n"

        record = make_record_text(log)
        text_message += record

    text_message += footer
    return text_message


def put_remarks_by_ids(remarks, log_ids: str):

    ids = log_ids.slpit(",")
    logs = Log.objects.filter(id__in=ids)
    for log in logs:
        log.remarks = remarks
        log.save()


def get_logs_by_user_id(user_id, limit: int):

    member = Member.objects.get_or_none(telegram_id=user_id)
    if member:
        logs = Log.objects.filter(member_fk=member).order_by("-created")[:limit]
        rows = map(return_row, logs)
        return rows


def edit_history(log_id):
    log = Log.objects.get_or_none(id=log_id)
    history = log.edit_history if log.edit_history else ""
    status = log.status
    history += f"Edited at {datetime.now()} for {status}\n"
    log.history = history
    log.save()
    return status, history
