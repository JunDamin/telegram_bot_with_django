from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):

    """ Member Admin Definition """

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
    )

    list_filter = ("is_active",)

