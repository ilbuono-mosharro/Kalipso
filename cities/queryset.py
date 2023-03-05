from django.db import models


class CityQuerySet(models.QuerySet):
    def active_cities(self):
        return self.filter(is_active=True).only('id', 'name')
