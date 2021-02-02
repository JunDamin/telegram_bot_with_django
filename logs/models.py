from django.db import models
from core import models as core_models
from staff.models import Member


class WorkingDay(core_models.TimeStampedModel):
    date = models.DateField()

    def __str__(self):
        return self.date.isoformat()


class Log(core_models.TimeStampedModel):

    STATUS_SIGN_IN = "signing in"
    STATUS_SIGN_OUT = "signing out"
    STATUS_GET_BACK = "getting back"

    STATUS_CHOICES = (
        (STATUS_SIGN_IN, "Signing In"),
        (STATUS_SIGN_OUT, "Signing Out"),
        (STATUS_GET_BACK, "Getting Back"),
    )

    member_fk = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='log')
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    optional_status = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    distance = models.CharField(max_length=100, null=True, blank=True)
    confirmation = models.TextField(null=True, blank=True)    
    remarks = models.TextField(null=True, blank=True)
    edit_history = models.TextField(null=True, blank=True)
    working_day = models.ForeignKey(WorkingDay, on_delete=models.PROTECT, related_name="log", null=True)
    
    def __str__(self):
        return f"No.{self.id} : {self.local_date()} | {self.member_fk} | {self.status}"

    def local_date(self):
        return self.timestamp.astimezone(self.member_fk.office_fk.office_timezone).strftime("%Y.%m.%d")

    def local_weekday(self):
        return self.timestamp.astimezone(self.member_fk.office_fk.office_timezone).strftime("%A")   

    def local_time(self):
        return self.timestamp.astimezone(self.member_fk.office_fk.office_timezone).strftime("%H:%M")

    def content(self):
        return f"No.{self.work_content.id}" if hasattr(self, "work_content") else "-"


class WorkContent(core_models.TimeStampedModel):
    log_fk = models.OneToOneField(Log, on_delete=models.CASCADE, related_name="work_content", null=True)
    content = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)


class Leave(core_models.TimeStampedModel):
    member_fk = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='leave')
    start_date = models.DateField()
    end_date = models.DateField()
    leave_days = models.IntegerField()
    working_days = models.ManyToManyField(WorkingDay, related_name="leave", null=True)
    confirmed = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.start_date.isoformat()} - {self.end_date.isoformat()}"


class HalfDayOff(core_models.TimeStampedModel):
    date = models.DateField()
    off_hour = models.IntegerField()
    working_day = models.ManyToManyField(WorkingDay, related_name="half_day_off", null=True)
    confirmed = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)

    def leave_days(self):
        return self.off_hour / 8
