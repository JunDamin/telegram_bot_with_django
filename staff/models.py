from django.db import models
from core import models as core_models


class Member(core_models.TimeStampedModel):
    id = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    koica_id = models.CharField(max_length=100, null=True, blank=True)
    office_fk = models.ForeignKey("offices.Office", related_name="member", on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return " ".join([self.first_name, self.last_name])
