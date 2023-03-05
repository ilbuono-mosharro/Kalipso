from django.db import models
from django.utils.translation import gettext_lazy as _

from ads.models import Standard


# Create your models here.
class Auto(Standard):
    class AdTypeChoice(models.TextChoices):
        empty = "", "Select ad type"
        SALE = 'SA', _('For sale')
        RENT = 'RE', _('For rent')

    class TransmissionTypeChoice(models.TextChoices):
        empty = "", "Select transmission"
        MANUAL = 'ML', _('Manual')
        AUTOMATIC = 'AC', _('Automatic')
        CVT = 'CVT', _('CVT')

    class FuelTypeChoice(models.TextChoices):
        empty = "", "Select fuel"
        PETROL = 'PL', _('Petrol')
        DIESEL = 'DL', _('Diesel')
        BIFUEL = 'BL', _('Bi-fuel')
        ELECTRIC = 'EC', _('Electric')
        HYBRID = 'HD', _('Hybrid')

    class DoorsChoice(models.TextChoices):
        empty = "", "Select doors"
        ZERO = 0, _('0 doors')
        ONE = 1, _('1 door')
        TWO = 2, _('2/3 doors')
        FOUR = 4, _('4/5 doors')
        SIX = 6, _('6/7 doors')

    class DriveTypeChoice(models.TextChoices):
        empty = "", "Select drive type"
        TWO = 0, _('4x2')
        FOUR = 1, _('4x4')
        FRONT = 2, _('Front wheel drive')
        REAR = 4, _('Rear wheel drive')

    make = models.CharField(max_length=50)
    doors = models.CharField(max_length=5, choices=DoorsChoice.choices)
    seats = models.PositiveSmallIntegerField(blank=True)
    fuel = models.CharField(max_length=20, choices=FuelTypeChoice.choices)
    transmission = models.CharField(max_length=9, choices=TransmissionTypeChoice.choices)
    consumption = models.CharField(max_length=150)
    kms_driven = models.PositiveSmallIntegerField()
    first_registration = models.CharField(max_length=8)
    drive_type = models.CharField(max_length=8, choices=DriveTypeChoice.choices)
    ad_type = models.CharField(max_length=20, choices=AdTypeChoice.choices)


class Moto(Standard):
    class AdTypeChoice(models.TextChoices):
        empty = "", "Select ad type"
        SALE = 'SA', _('For sale')
        RENT = 'RE', _('For rent')

    class TransmissionTypeChoice(models.TextChoices):
        empty = "", "Select transmission"
        MANUAL = 'ML', _('Manual')
        AUTOMATIC = 'AC', _('Automatic')
        CVT = 'CVT', _('CVT')

    class FuelTypeChoice(models.TextChoices):
        empty = "", "Select fuel"
        PETROL = 'PL', _('Petrol')
        DIESEL = 'DL', _('Diesel')
        BIFUEL = 'BL', _('Bi-fuel')
        ELECTRIC = 'EC', _('Electric')
        HYBRID = 'HD', _('Hybrid')

    make = models.CharField(max_length=50)
    fuel = models.CharField(max_length=20, choices=FuelTypeChoice.choices)
    transmission = models.CharField(max_length=9, choices=TransmissionTypeChoice.choices)
    consumption = models.CharField(max_length=150)
    kms_driven = models.PositiveSmallIntegerField()
    first_registration = models.CharField(max_length=8)
    ad_type = models.CharField(max_length=20, choices=AdTypeChoice.choices)
