from django.db import models
from core import models as core_models
from chats.models import Chat
from staff.models import Member
# Create your models here.


class Log(core_models.TimeStampedModel):

    STATUS_SIGN_IN = "signing in"
    STATUS_SIGN_OUT = "signing out"
    STATUS_GET_BACK = "getting back"

    STATUS_CHOICES = (
        (STATUS_SIGN_IN, "Signing In"),
        (STATUS_SIGN_OUT, "Signing Out"),
        (STATUS_GET_BACK, "Getting Back"),
    )

    chat_fk = models.ForeignKey(Chat, on_delete=models.PROTECT, related_name="log")
    member_fk = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='log')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    log_datetime = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    optional_status = models.CharField(max_length=100, null=True)
    longitude = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=100, null=True)
    remarks = models.TextField(null=True)
    confirmation = models.CharField(max_length=100, null=True)
    edit_history = models.TextField(null=True)

    def __str__(self):
        return f"{self.log_datetime.isoformat()} {self.first_name}"


class WorkContent(core_models.TimeStampedModel):
    member_fk = models.ForeignKey(Member, on_delete=models.CASCADE)
    log_fk = models.OneToOneField(Log, on_delete=models.CASCADE, related_name="work_content", null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)    
    content = models.TextField(null=True)
    remarks = models.TextField(null=True)
