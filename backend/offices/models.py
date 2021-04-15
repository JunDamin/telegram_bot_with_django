from django.db import models
from django_countries.fields import CountryField
from timezone_field import TimeZoneField
from core import models as core_models


class Office(core_models.TimeStampedModel):
    name_kr = models.CharField(max_length=100)
    name_en = models.CharField(max_length=200, null=True)
    code = models.IntegerField(null=True, blank=True)
    country = CountryField()
    timezone = TimeZoneField()
    open_time = models.TimeField(null=True)
    close_time = models.TimeField(null=True)

    def __str__(self):
        return self.name_kr

# Holiday field?
