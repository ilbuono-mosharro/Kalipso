from django.db import models


class CategoryQuerySet(models.QuerySet):
    def active_categories_home(self):
        return self.filter(is_active=True).values('bg_class_name', 'icon', 'name', 'slug')

    def active_categories_searchbar(self):
        return self.filter(is_active=True).only('name', 'slug').order_by('name')

    def active_categories(self):
        return self.filter(is_active=True).select_related('user').prefetch_related('category_in_sub')