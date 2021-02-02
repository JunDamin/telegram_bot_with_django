import os
import django
import dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
dotenv.read_dotenv()
django.setup()


import sqlite3
from pprint import pprint
from logs.models import Log, WorkingDay
from staff.models import Member
from offices.models import Office
from datetime import datetime


office = Office.objects.all()[0]

logs = Log.objects.all()
WorkingDay.objects.all().delete()

for log in logs:
    print(log.timestamp.date(), type(log.timestamp.date()))
    working_day, _ = WorkingDay.objects.get_or_create(date=log.timestamp.date())
    log.working_day = working_day
    log.save()
