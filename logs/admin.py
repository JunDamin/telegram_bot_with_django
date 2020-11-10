from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Log)
class LogAdmin(admin.ModelAdmin):

    """ Log Admin Definition """

    list_display = (
        "id",
        "member_fk",
        "local_date",
        "local_time",
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
        "content",
        "remarks",
    )

    list_filter = ("log_fk__status",)