from django.db import models
from django.utils.translation import gettext_lazy as _
from ads.models import Announcement


# # Create your models here.
class Properties(Announcement):
    class AdTypeChoice(models.TextChoices):
        SALE = 'SA', _('For sale')
        RENT = 'RE', _('For rent')

    ad_type = models.CharField(max_length=20, choices=AdTypeChoice.choices)
    square_feet = models.PositiveSmallIntegerField()


class House(Properties):
    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
