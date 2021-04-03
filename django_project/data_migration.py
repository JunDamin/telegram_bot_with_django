import os
import django
import dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
dotenv.read_dotenv()
django.setup()


import sqlite3
from pprint import pprint
from logs.models import Log
from staff.models import Member
from offices.models import Office
from datetime import datetime

db_path = os.environ['DB_PATH']

print("db:", db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT * FROM logbook;")
rows = cursor.fetchall()


info = cursor.execute("PRAGMA table_info(logbook);")
info = cursor.fetchall()

header_name = list(map(lambda x: x[1], info))
print(header_name)

data_list = []
for row in rows:
    data_list.append({col: value for col, value in zip(header_name, row)})


office = Office.objects.all()[0]

for data in data_list:
    print('log {} start', data['id'])
    pprint(data)
    (member, _) = Member.objects.get_or_create(
        id=data["chat_id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        office_fk=office,
    )
    log = Log(
        created=datetime.now(),
        id=data["id"],
        member_fk=member,
        timestamp=data["timestamp"],
        status=data["category"],
        optional_status=data['sub_category'],
        longitude=data['longitude'],
        latitude=data['latitude'],
        confirmation=data['confirmation'],
        edit_history=data['history'],
        remarks=data['remarks']
    )
    log.save()
    print('log {} saved', data['id'])
conn.close()