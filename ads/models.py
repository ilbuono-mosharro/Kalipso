import random
import string
import uuid

from django.conf import settings
from django.core.validators import validate_slug, FileExtensionValidator, validate_image_file_extension, \
    validate_ipv46_address
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile
from accounts.utils import validate_file_size
from categories.models import Category, SubCategory
from cities.models import Cities
from .utils import user_directory_path
from .queryset import AnnouncementQuerySet


def generate_unique_code():
    unique_code = ''.join(random.choices(string.digits, k=10))
    try:
        Announcement.objects.get(unique_code=unique_code)
        return generate_unique_code()
    except Announcement.DoesNotExist:
        return unique_code


# Create your models here.
class Announcement(models.Model):
    class AdsStatus(models.TextChoices):
        APPROVED = 'AP', _('Approved')
        REJECT = 'RE', _('Reject')
        WAITING = 'WA', _('Waiting')
        DEACTIVE = 'DE', _('Deactive')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='announcement_user_profile')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="announcement_category")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="announcement_subcategory")
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name="announcement_city")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, validators=[validate_slug], unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ip = models.GenericIPAddressField(validators=[validate_ipv46_address])
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="users_wishlist", blank=True)
    visits = models.SmallIntegerField(blank=True, default=0)
    status = models.CharField(max_length=8, choices=AdsStatus.choices, default=AdsStatus.WAITING)
    unique_code = models.CharField(max_length=10, default=generate_unique_code, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()  # The default manager.
    ad_manager = AnnouncementQuerySet.as_manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = generate_unique_code()
        self.slug = slugify(self.title)
        super(Announcement, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at",)


    def get_absolute_url(self):
        return reverse('ads:announcement_detail', args=[self.slug])


class Standard(Announcement):
    class ConditionTypeChoice(models.TextChoices):
        empty = "", "Select condition"
        USED = 'UD', _('Used')
        NEW = 'NW', _('New')

    condition = models.CharField(max_length=4, choices=ConditionTypeChoice.choices)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="announcement_images")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_profile_images_announcement')
    image = models.ImageField(upload_to=user_directory_path, validators=[
        validate_image_file_extension, FileExtensionValidator(['JPEG', 'JPG', 'PNG']), validate_file_size
    ])
    alt_text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    ip = models.GenericIPAddressField(validators=[validate_ipv46_address])
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
