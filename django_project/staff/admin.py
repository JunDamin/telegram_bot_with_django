from django.contrib import admin
from . import models
from logs.models import Log
# Register your models here.


class LogInline(admin.TabularInline):
    model = Log
    extra = 0

@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):

    """ Member Admin Definition """
    inlines = [LogInline]

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": ("id", "first_name", "last_name",)},
        ),
        ("Extra Info", {"fields": ("koica_id", "office_fk", "is_active")},),
    )

    list_display = (
        "id",
        "first_name",
        "last_name",
        "koica_id",
        "office_fk",
        "is_active",
        "full_name",
        "used_leave_in_this_year",
        "used_leave_of_last_year",
    )

    list_filter = ("is_active",)

