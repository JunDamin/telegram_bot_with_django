from offices.models import Office
from chats.models import Chat
from logs.models import Log
from staff.models import Member
from datetime import datetime
import pytz
from django.utils.timezone import make_aware

tz = pytz.timezone("Africa/Douala")

new_office = Office(office_name_kr="카메룬 사무소", office_name_en="Cameroon KOICA Office", office_timezone="Duala")
new_office.save()
print(new_office)

new_chat = Chat(chat_id="13012319", chat_name="두번째테스트", office_fk=new_office, is_active=True)
new_chat.save()
print(new_chat)

new_member = Member(telegram_id="1234", first_name="전", last_name="다민", office_fk=new_office)
new_member.save()
print(new_member)

new_log = Log(chat_fk=new_chat, member_fk=new_member, first_name=new_member.first_name, last_name=new_member.last_name, status="signing in", log_datetime="2020-11-22 12:11")
print(new_log)
new_log.save()

log = Log.objects.filter(first_name='전').last()
log.optional_status = "test"
log.save()
