from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Log)
class LogAdmin(admin.ModelAdmin):

    """ Log Admin Definition """

    list_display = (
        "chat_id",
        "telegram_id", 
        "first_name",
        "last_name",
        "log_datetime",
        "status",
        "optional_status",
        "longitude",
        "latitude",
        "remarks",
        "confirmation",
        "edit_history",
    )

    list_filter = ("status",)