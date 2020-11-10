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
        "office_name_kr",
        "office_name_en", 
        "office_code",
        "office_country",
        "office_open_time",
        "office_close_time",
    )
