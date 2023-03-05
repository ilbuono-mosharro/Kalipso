import uuid

from django.conf import settings
from django.core.validators import validate_slug
from django.db import models
from .queryset import CityQuerySet


# Create your models here.
class Cities(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_city')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, validators=[validate_slug])
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()  # The default manager.
    city_manager = CityQuerySet.as_manager()

    def __str__(self):
        return self.name
