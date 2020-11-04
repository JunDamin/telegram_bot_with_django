from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Member)
class ReservationAdmin(admin.ModelAdmin):

    """ Member Admin Definition """

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": ("telegram_id", "first_name", "last_name",)},
        ),
        ("Extra Info", {"fields": ("koica_id", "office_fk", "is_active")},),
    )

    list_display = (
        "telegram_id",
        "first_name",
        "last_name",
        "koica_id",
        "office_fk",
        "is_active",
    )

    list_filter = ("is_active",)

