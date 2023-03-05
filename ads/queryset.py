from django.db import models


class AnnouncementQuerySet(models.QuerySet):
    def active_ad(self):
        return self.filter(status="AP").select_related(
            'profile', 'category', 'subcategory', 'city', 'standard', 'standard__auto', 'standard__moto', 'jobs',
            'properties', 'properties__house', 'profile__user',
        ).prefetch_related(
            'users_wishlist', 'announcement_images',
        )
