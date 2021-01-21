from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from import_export import resources
from import_export.admin import ImportExportMixin, ExportActionMixin
from import_export.fields import Field
from import_export.widgets import DateTimeWidget
from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter
from . import models
from staff import models as staff_models

class StatusListFilter(MultipleChoiceListFilter):
    title = 'Status'
    parameter_name = 'status__in'

    def lookups(self, requests, modle_admin):
        return models.Log.STATUS_CHOICES


class MemberListFilter(MultipleChoiceListFilter):
    title = 'Member'
    parameter_name = 'member_fk__in'

    def lookups(self, requests, modle_admin):
        return staff_models.Member.objects.values_list('pk', 'first_name')


class LogResource(resources.ModelResource):
    local_datetime = Field()
    local_weekday = Field()

    class Meta:
        model = models.Log
        fields = (
            "id",
            "member_fk",
            "member_fk__first_name",
            "member_fk__last_name",
            "local_datetime",
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
            "local_datetime",
            "local_weekday",
            "status",
            "optional_status",
            "longitude",
            "latitude",
            "remarks",
            "confirmation",
            "edit_history",
        )

    def dehydrate_local_datetime(self, log):
        return "%s %s" % (log.local_date(), log.local_time())

    def dehydrate_local_weekday(self, log):
        return "%s" % log.local_weekday()


class ContentInline(admin.TabularInline):
    model = models.WorkContent
    extra = 0


@admin.register(models.Log)
class LogAdmin(ImportExportMixin, ExportActionMixin, admin.ModelAdmin):

    """ Log Admin Definition """
    inlines = [ContentInline, ]
    resource_class = LogResource

    list_display = (
        "id",
        "member_fk",
        "local_date",
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

