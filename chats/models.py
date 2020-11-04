from django.db import models
from offices import models as office_model

# Create your models here.
class Chat(models.Model):
    chat_id = models.CharField(max_length=100, primary_key=True)
    chat_name = models.CharField(max_length=100)
    office_fk = models.ForeignKey("offices.Office", related_name="chat", on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField()