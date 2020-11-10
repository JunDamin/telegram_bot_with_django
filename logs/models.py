from django.db import models
from core import models as core_models
from staff.models import Member


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
    log_datetime = models.DateTimeField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    optional_status = models.CharField(max_length=100, null=True)
    longitude = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=100, null=True)
    remarks = models.TextField(null=True)
    confirmation = models.CharField(max_length=100, null=True)
    edit_history = models.TextField(null=True)

    def __str__(self):
        return f"{self.id} {self.log_datetime}"

    def local_date(self):
        return self.log_datetime.astimezone(self.member_fk.office_fk.office_timezone).strftime("%m-%d")

    def local_time(self):
        return self.log_datetime.astimezone(self.member_fk.office_fk.office_timezone).strftime("%H:%M")


class WorkContent(core_models.TimeStampedModel):
    log_fk = models.OneToOneField(Log, on_delete=models.CASCADE, related_name="work_content", null=True)
    content = models.TextField(null=True)
    remarks = models.TextField(null=True)
