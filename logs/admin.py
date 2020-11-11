from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from import_export import resources
from import_export.admin import ImportExportMixin, ExportActionMixin
from import_export.fields import Field
from import_export.widgets import DateTimeWidget
from . import models


class LogResource(resources.ModelResource):
    local_datetime = Field()

    class Meta:
        model = models.Log
        fields = (
            "id",
            "member_fk",
            "member_fk__first_name",
            "member_fk__last_name",
            "local_datetime",
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
        "status",
        "optional_status",
        "longitude",
        "latitude",
        "remarks",
        "confirmation",
        "edit_history",
        "content",
    )

    list_filter = (
        "timestamp",
        ("timestamp", DateRangeFilter),
        "status",
        "optional_status",
    )


@admin.register(models.WorkContent)
class WorkContentAdmin(admin.ModelAdmin):

    """ Work Content Admin Definition """

    list_display = (
        "log_fk",
        "content",
        "remarks",
    )

    list_filter = ("log_fk__status",)

