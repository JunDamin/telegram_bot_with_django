import os
import django
import dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
dotenv.read_dotenv()
django.setup()

from math import sqrt
from logs.models import Log

def check_distance(log):
    session = log.status
    if session == "signing out":
        # set variable
        member = log.member_fk
        date = log.timestamp.date()

        log_out = log
        log_in = Log.objects.get_or_none(member_fk=member, timestamp__date=date, status="signing in")

        print(log_out, log_in)

        if log_out and log_in:
            x1, y1 = log_out.longitude, log_out.latitude
            x2, y2 = log_in.longitude, log_in.latitude

            if x1 == "Not Available" or x2 == "Not Available":
                output = "Not Available"
            elif x1 and y1 and x2 and y2:
                x1, y1 = map(float, (x1, y1))
                x2, y2 = map(float, (x2, y2))
                distance = sqrt((x1-x2)**2 + (y1-y2)**2)
                if distance < 0.003:
                    output = "OK"
                else:
                    output = "Need to Check"
            else:
                output = "error"
            log_out.distance = output

        if not log_in:
            log_out.distance = "No Log in"

        log_out.save()


for log in Log.objects.all():
    check_distance(log)
