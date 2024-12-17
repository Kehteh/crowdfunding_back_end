from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Sum

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.PositiveIntegerField()
    image = models.URLField(blank=True, null=True)
    is_open = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )

    @property
    def total_pledged(self):
        return self.pledges.aggregate(total=Sum('amount'))['total'] or 0

    def __str__(self):
        return f"Project({self.title}, Goal={self.goal})"


class Pledge(models.Model):
    amount = models.PositiveIntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField(default=False, db_index=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name='pledges',
        null=True,
        blank=True
    )

    def clean(self):
        if self.anonymous and self.supporter is not None:
            raise ValidationError("An anonymous pledge should not have a supporter associated with it.")
        if self.amount <= 0:
            raise ValidationError("Pledge amount must be greater than zero.")
        if self.project and not self.project.is_open:
            raise ValidationError("You cannot pledge to a closed project.")

    def __str__(self):
        return f"Pledge({self.amount}, Anonymous={self.anonymous})"
   