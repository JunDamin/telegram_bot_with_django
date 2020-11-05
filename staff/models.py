from django.db import models

# Create your models here.

class Member(models.Model):
    telegram_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    koica_id = models.CharField(max_length=100, null=True)
    office_fk = models.ForeignKey("offices.Office", related_name="member", on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    

