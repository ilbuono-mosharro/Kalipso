from django.db import models
from django.utils.translation import gettext_lazy as _

from ads.models import Announcement


# Create your models here.
class Jobs(Announcement):
    class JobScheduleChoice(models.TextChoices):
        empty = "", "Select schedule"
        PART_TIME = 'PE', _('Part Time')
        FULL_TIME = 'FE', _('Full Time')

    class JobLevelChoice(models.TextChoices):
        empty = "", "Select level"
        IN_PERSON = 'PE', _('In-Person')
        REMOTE = 'FE', _('Remote')
        HYDRID = 'HD', _('Hybrid')

    schedule = models.CharField(max_length=9, choices=JobScheduleChoice.choices)
    level = models.CharField(max_length=9, choices=JobLevelChoice.choices)
