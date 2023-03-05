from django.contrib import sitemaps
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from ads.models import Announcement
from categories.models import Category, SubCategory
from cities.models import Cities

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['pages:home', 'pages:privacy', 'pages:cookie', 'pages:terms']

    def location(self, item):
        return reverse(item)


class AnnouncementSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Announcement.ad_manager.active_ad()

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Category.category_manager.active_categories()

    def lastmod(self, obj):
        return obj.updated_at


class SubCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return SubCategory.objects.select_related('category').filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

