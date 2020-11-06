from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Log)
class LogAdmin(admin.ModelAdmin):

    """ Log Admin Definition """

    list_display = (
        "chat_fk",
        "member_fk",
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


@admin.register(models.WorkContent)
class WorkContentAdmin(admin.ModelAdmin):

    """ Work Content Admin Definition """

    list_display = (
        "log_fk",
        "member_fk",
        "first_name",
        "last_name",
        "content",
        "remarks",
    )

    list_filter = ("member_fk",)