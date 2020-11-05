from django.db import models

# Create your models here.

class Office(models.Model):
    office_name_kr = models.CharField(max_length=100)
    office_name_en = models.CharField(max_length=200, null=True)
    office_code = models.IntegerField(null=True)
    office_timezone = models.CharField(max_length=100, null=True)
    office_open_time = models.TimeField(null=True)
    office_close_time = models.TimeField(null=True)

    def __str__(self):
        return self.office_name_kr