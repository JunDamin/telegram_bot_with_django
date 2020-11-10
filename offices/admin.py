from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Office)
class OfficeAdmin(admin.ModelAdmin):

    """ Office Admin Definition """

    list_display = (
        "office_name_kr",
        "office_name_en", 
        "office_code",
        "office_country",
        "office_open_time",
        "office_close_time",
    )
