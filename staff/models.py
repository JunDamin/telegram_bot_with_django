from django.db import models

# Create your models here.

class Member(models.Model):
    telegram_id = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    koica_id = models.CharField(max_length=100, null=True)
    office_fk = models.ForeignKey("offices.Office", related_name="member", on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return " ".join([self.first_name, self.last_name])
