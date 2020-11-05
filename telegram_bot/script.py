from offices.models import Office
from chats.models import Chat
from logs.models import Log

new_office = Office(office_name_kr="카메룬 사무소", office_name_en="Cameroon KOICA Office", office_timezone="Duala")
new_office.save()

new_chat = Chat(chat_id="13012319", chat_name="두번째테스트", office_fk=new_office, is_active=True)
new_chat.save()

new_log = Log()

