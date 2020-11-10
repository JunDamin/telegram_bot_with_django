from django.db import models
from django_countries.fields import CountryField
from timezone_field import TimeZoneField
from core import models as core_models


class Office(core_models.TimeStampedModel):
    office_name_kr = models.CharField(max_length=100)
    office_name_en = models.CharField(max_length=200, null=True)
    office_code = models.IntegerField(null=True)
    office_country = CountryField()
    office_timezone = TimeZoneField()
    office_open_time = models.TimeField(null=True)
    office_close_time = models.TimeField(null=True)

    def __str__(self):
        return self.office_name_kr
