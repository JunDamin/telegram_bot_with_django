from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):

    """ Chat Admin Definition """

    list_display = (
        "id",
        "chat_name", 
        "office_fk",
        "is_active",
    )

    list_filter = ("is_active",)