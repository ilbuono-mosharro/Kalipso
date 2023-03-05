from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Individual, Company


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.u_type == "CO":
            Company.objects.create(user=instance)
        else:
            Individual.objects.create(user=instance)
