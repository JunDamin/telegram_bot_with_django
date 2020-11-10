from django.db import models
from core import models as core_models


class Chat(core_models.TimeStampedModel):
    id = models.CharField(max_length=100, primary_key=True)
    chat_type = models.CharField(max_length=20)
    chat_name = models.CharField(max_length=100, null=True)
    office_fk = models.ForeignKey(
        "offices.Office", related_name="chat", on_delete=models.CASCADE, null=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.chat_name if self.chat_name else "Untitle"
