from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from import_export import resources
from import_export.admin import ImportExportMixin, ExportActionMixin
from import_export.fields import Field
from import_export.widgets import DateTimeWidget
from django_admin_multiple_choice_list_filter.list_filters import (
    MultipleChoiceListFilter,
)
from . import models
from staff import models as staff_models


class StatusListFilter(MultipleChoiceListFilter):
    title = "Status"
    parameter_name = "status__in"

    def lookups(self, requests, modle_admin):
        return models.Log.STATUS_CHOICES


class MemberListFilter(MultipleChoiceListFilter):
    title = "Member"
    parameter_name = "member_fk__in"

    def lookups(self, requests, modle_admin):
        return staff_models.Member.objects.values_list("pk", "first_name")


class LogResource(resources.ModelResource):
    local_time = Field()
    local_weekday = Field()

    class Meta:
        model = models.Log
        fields = (
            "id",
            "member_fk",
            "member_fk__first_name",
            "member_fk__last_name",
            "working_day__date",
            "local_time",
            "local_weekday",
            "status",
            "optional_status",
            "longitude",
            "latitude",
            "remarks",
            "confirmation",
            "edit_history",
        )
        export_order = (
            "id",
            "member_fk",
            "member_fk__first_name",
            "member_fk__last_name",
            "working_day__date",
            "local_time",
            "local_weekday",
            "status",
            "optional_status",
            "longitude",
            "latitude",
            "remarks",
            "confirmation",
            "edit_history",
        )

    def dehydrate_local_time(self, log):
        return log.local_time()

    def dehydrate_local_weekday(self, log):
        return "%s" % log.local_weekday()


class ContentInline(admin.TabularInline):
    model = models.WorkContent
    extra = 0


@admin.register(models.Log)
class LogAdmin(ImportExportMixin, ExportActionMixin, admin.ModelAdmin):

    """ Log Admin Definition """

    inlines = [
        ContentInline,
    ]
    resource_class = LogResource

    list_display = (
        "id",
        "member_fk",
        "working_day",
        "local_time",
        "local_weekday",
        "status",
        "optional_status",
        "distance",
        "remarks",
        "edit_history",
        "content",
    )

    list_filter = (
        "timestamp",
        ("timestamp", DateRangeFilter),
        StatusListFilter,
        MemberListFilter,
        "distance",
    )


@admin.register(models.WorkContent)
class WorkContentAdmin(admin.ModelAdmin):

    """ Work Content Admin Definition """

    list_display = (
        "id",
        "log_fk",
        "content",
        "remarks",
    )

    list_filter = ("log_fk__status",)


@admin.register(models.WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):

    """ Work Content Admin Definition """

    list_display = ("date",)

    list_filter = (("date", DateRangeFilter),)


@admin.register(models.Leave)
class LeaveAdmin(admin.ModelAdmin):

    """ Work Content Admin Definition """
    fieldsets = (
        ("basic", {
            'fields': ('start_date', 'end_date', 'leave_days')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('confirmed',),
        }),
    )

    list_display = ("member_fk", "start_date", "end_date", "leave_days", "used_day", "confirmed")

    list_filter = (
        ("start_date", DateRangeFilter),
        ("end_date", DateRangeFilter),
    )