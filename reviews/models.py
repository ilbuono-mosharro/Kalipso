from django.conf import settings
from django.core.validators import MaxValueValidator, validate_ipv46_address, MinValueValidator
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile


# Create your models here.
class ReviewRating(models.Model):
    class ReviewStatus(models.TextChoices):
        APPROVED = 'AP', _('Approved')
        REJECT = 'RE', _('Reject')
        WAITING = 'WA', _('Waiting')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='review_profile')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_review')
    subject = models.CharField(max_length=100)
    review = models.TextField(max_length=500)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    ip = models.GenericIPAddressField(validators=[validate_ipv46_address])
    status = models.CharField(max_length=8, choices=ReviewStatus.choices, default=ReviewStatus.WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ('-created_at',)
