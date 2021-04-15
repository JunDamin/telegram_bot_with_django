from django.contrib import admin
from . import models
from staff import models as staff_models
# Register your models here.

class MemberInline(admin.TabularInline):
    model = staff_models.Member
    extra = 0


@admin.register(models.Office)
class OfficeAdmin(admin.ModelAdmin):

    """ Office Admin Definition """
    inlines = [MemberInline, ]
    list_display = (
        "name_kr",
        "name_en", 
        "code",
        "country",
        "open_time",
        "close_time",
    )
