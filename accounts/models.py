import random
import string
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, validate_image_file_extension, validate_ipv46_address
from django.db import models
from django.db.models import Count, Avg, Q
from django.utils.translation import gettext_lazy as _

from cities.models import Cities
from .utils import validate_file_size, user_directory_path


# Create your models here.
class User(AbstractUser):
    class UserTypeChoice(models.TextChoices):
        COMPANY = 'CO', _('Company')
        INDIVIDUAL = 'PE', _('Individual Person')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    u_type = models.CharField(max_length=20, choices=UserTypeChoice.choices)
    email_confirmation = models.BooleanField(default=False)
    terms_and_privacy = models.BooleanField()
    ip = models.GenericIPAddressField(validators=[validate_ipv46_address])


def generate_unique_code():
    unique_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    try:
        Profile.objects.get(unique_code=unique_code)
        return generate_unique_code()
    except Profile.DoesNotExist:
        return unique_code


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="user_profile_related",
                                related_query_name="user_profile", )
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name="user_city", blank=True, null=True)
    avatar = models.ImageField(upload_to=user_directory_path, validators=[
        validate_image_file_extension, FileExtensionValidator(['JPEG', 'JPG', 'PNG']), validate_file_size,
    ], blank=True, null=True)
    unique_code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    phone = models.CharField(max_length=9, blank=True, null=True)
    hidden_phone = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def count_ad_by_status(self):
        return self.announcement_user_profile.aggregate(
            published=Count('id', filter=Q(status="AP")),
            waiting=Count('id', filter=Q(status="WA")),
            reject=Count('id', filter=Q(status="RE")),
        )

    def get_reviews_avg(self):
        return self.review_profile.select_related('profile', 'user').filter(status="AP").aggregate(
            review_number=Count('id'), review_avg=Avg('rating')
        )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = generate_unique_code()
        super().save(*args, **kwargs)


class Individual(Profile):
    class GenderChoices(models.TextChoices):
        empty = "", "Select gender"
        MALE = 'ML', _('Male')
        FEMALE = 'FM', _('Female')
        OTHER = 'OTH', _('Other')
        PREFER_NOT_TO_SAY = 'PS', _('Prefer Not To Say')

    gender = models.CharField(max_length=3, choices=GenderChoices.choices, default=GenderChoices.PREFER_NOT_TO_SAY)

    def __str__(self):
        return f"Profile of {self.user.username}"

    class Meta:
        verbose_name = "Individual Person"
        verbose_name_plural = "Individual Persons"


class Company(Profile):
    name = models.CharField(max_length=200)
    vat_number = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=4)

    def __str__(self):
        return f"Profile {self.user.username} - {self.name}"

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
