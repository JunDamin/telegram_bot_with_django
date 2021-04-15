from django.db import models
from core import models as core_models
from django.utils import timezone


class Member(core_models.TimeStampedModel):
    id = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    koica_id = models.CharField(max_length=100, null=True, blank=True)
    office_fk = models.ForeignKey(
        "offices.Office", related_name="member", on_delete=models.SET_NULL, null=True
    )
    is_active = models.BooleanField(default=True)
    yearly_leave = models.FloatField(null=True)

    def __str__(self):
        return " ".join([self.first_name, self.last_name])

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def used_leave_in_this_year(self):
        Q = models.Q
        now = timezone.now()
        leaves = self.leaves.filter(
            Q(working_days__date__year=now.year)
        )
        leave_days = []
        for leave in leaves:
            leave_days.append(leave.working_days.filter(date__year=now.year))

        return len(leave_days)


    def used_leave_of_last_year(self):
        ## 실제 등록된 시간과 register 된 working day 간의 차이가 발생할 경우 어떻게 해야 하는가?
        Q = models.Q
        now = timezone.now()
        leaves = self.leaves.filter(
            Q(working_days__date__year=now.year-1)
        )
        print(leaves)
        leave_days = []
        for leave in leaves:
            leave_days.append(leave.working_days.filter(date__year=now.year-1))

        return len(leave_days)
