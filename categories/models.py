import uuid

from django.conf import settings
from django.core.validators import validate_slug
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from .queryset import CategoryQuerySet


class ManageForms(models.Model):
    active_form_standard = models.BooleanField(default=False)
    active_form_auto = models.BooleanField(default=False)
    active_form_moto = models.BooleanField(default=False)
    active_form_jobs = models.BooleanField(default=False)
    active_form_properties = models.BooleanField(default=False)
    active_form_apartments = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ManageFilters(models.Model):
    filter_condition = models.BooleanField(default=False)
    filter_transmissions = models.BooleanField(default=False)
    filter_fuels = models.BooleanField(default=False)
    filter_ad_types = models.BooleanField(default=False)
    filter_schedules = models.BooleanField(default=False)
    filter_levels = models.BooleanField(default=False)
    filter_price_min = models.BooleanField(default=False)
    filter_price_max = models.BooleanField(default=False)

    class Meta:
        abstract = True


# Create your models here.
class Category(ManageFilters):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_category')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, validators=[validate_slug])
    is_active = models.BooleanField(default=False)
    icon = models.CharField(max_length=50)
    bg_class_name = models.CharField(max_length=50, default="bg-yellow")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()  # The default manager.
    category_manager = CategoryQuerySet.as_manager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def clean(self):
        if SubCategory.objects.filter(slug=self.slug).exists():
            raise ValidationError(
                'This slug already exists in the subcategory, it must be unique between the category and subcategory.'
            )

    def get_absolute_url(self):
        return reverse('ads:announcements_by_category', args=[self.slug])


class SubCategory(ManageFilters, ManageForms):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_subategory')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='category_in_sub')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, validators=[validate_slug])
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('name',)
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'

    def __str__(self):
        return self.name

    def clean(self):
        if Category.objects.filter(slug=self.slug).exists():
            raise ValidationError(
                'This slug already exists in the category, it must be unique between the category and subcategory.'
            )

    def get_absolute_url(self):
        return reverse('ads:announcements_by_subcategory', args=[self.category.slug, self.slug])
