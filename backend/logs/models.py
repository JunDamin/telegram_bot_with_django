from django.db import models
from django.utils import timezone
from core import models as core_models
from staff.models import Member


class WorkingDay(core_models.TimeStampedModel):
    date = models.DateField(unique=True)
    isOffday = models.BooleanField(default=False)

    def __str__(self):
        return self.date.isoformat()

    def save(self, *args, **kwargs):
        super(WorkingDay, self).save(*args, **kwargs)
        if self.isOffday:
            return None
        Q = models.Q
        leaves = Leave.objects.filter(
            Q(start_date__lte=self.date) & Q(end_date__gte=self.date)
        )
        for leave in leaves:
            leave.working_days.add(self)
            member = leave.member_fk
            log, _ = Log.objects.get_or_create(
                member_fk=member,
                timestamp=timezone.datetime.combine(
                    self.date, timezone.datetime.min.time()
                ),
                status="leave",
                optional_status="Full Day",
                longitude="Not Available",
                latitude="Not Available",
                working_day=self,
            )
            log.save()


class Log(core_models.TimeStampedModel):

    STATUS_SIGN_IN = "signing in"
    STATUS_SIGN_OUT = "signing out"
    STATUS_GET_BACK = "getting back"
    STATUS_LEAVE = "leave"

    STATUS_CHOICES = (
        (STATUS_SIGN_IN, "Signing In"),
        (STATUS_SIGN_OUT, "Signing Out"),
        (STATUS_GET_BACK, "Getting Back"),
        (STATUS_LEAVE, "Leave"),
    )

    member_fk = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="log")
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    optional_status = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    distance = models.CharField(max_length=100, null=True, blank=True)
    confirmation = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    edit_history = models.TextField(null=True, blank=True)
    working_day = models.ForeignKey(
        WorkingDay, on_delete=models.PROTECT, related_name="log", null=True
    )

    def __str__(self):
        return f"No.{self.id} : {self.local_date()} | {self.member_fk} | {self.status}"

    def local_date(self):
        return self.timestamp.astimezone(self.member_fk.office_fk.timezone).strftime(
            "%Y.%m.%d"
        )

    def local_weekday(self):
        return self.timestamp.astimezone(self.member_fk.office_fk.timezone).strftime(
            "%A"
        )

    def local_time(self):
        return self.timestamp.astimezone(self.member_fk.office_fk.timezone).strftime(
            "%H:%M"
        )

    def content(self):
        return f"No.{self.work_content.id}" if hasattr(self, "work_content") else "-"


class WorkContent(core_models.TimeStampedModel):
    log_fk = models.OneToOneField(
        Log, on_delete=models.CASCADE, related_name="work_content", null=True
    )
    content = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)


leave_options = [
    ("Full", "Full day"),
    ("Morning", "Morning off"),
    ("Aternoon", "Afternoon off"),
]


class Leave(core_models.TimeStampedModel):

    member_fk = models.ForeignKey(
        Member, on_delete=models.PROTECT, related_name="leave"
    )
    leave_type = models.CharField(max_length=12, choices=leave_options)
    start_date = models.DateField()
    end_date = models.DateField()
    working_days = models.ManyToManyField(WorkingDay, related_name="leave", null=True)
    confirmed = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.start_date.isoformat()} - {self.end_date.isoformat()}"

    def save(self, *args, **kwargs):
        super(Leave, self).save(*args, **kwargs)

        # Add working days
        Q = models.Q
        days = WorkingDay.objects.filter(
            Q(date__lte=self.end_date) & Q(date__gte=self.start_date)
        )
        self.working_days.clear()
        self.working_days.add(*days)

        # add log records
        for day in self.working_days.all():
            log, _ = Log.objects.get_or_create(
                member_fk=self.member_fk,
                timestamp=timezone.datetime.combine(
                    day.date, timezone.datetime.min.time()
                ),
                status="leave",
                optional_status=self.leave_type,
                longitude="Not Available",
                latitude="Not Available",
                working_day=day,
            )
            log.save()

        # Delete wrong record
        wrong_logs = Log.objects.filter(
            Q(member_fk=self.member_fk)
            & Q(status="leave")
            & ~Q(
                working_day__in=[
                    query
                    for queryset in map(
                        lambda leave: leave.working_days.all(),
                        self.member_fk.leave.all(),
                    )
                    for query in queryset
                    if query
                ]
            )
        )
        wrong_logs.delete()

    def used_day(self):
        return (
            len(self.working_days.filter(offday=False))
            if self.leave_type == "Full"
            else 0.5
        )
