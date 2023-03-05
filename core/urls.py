"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from accounts.forms import EmailValidationOnForgotPassword
from .sitemaps import StaticViewSitemap, AnnouncementSitemap, CategorySitemap, SubCategorySitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'static': StaticViewSitemap,
    'announcement_ad': AnnouncementSitemap,
    'categories': CategorySitemap,
    'subcategories': SubCategorySitemap,

}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls', namespace='pages')),
    path('', include('accounts.urls', namespace='accounts')),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword),
         name='password_reset'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('ads.urls', namespace='ads')),
    path('', include('engines.urls', namespace='engines')),
    path('', include('categories.urls', namespace='categories')),
    path('', include('jobs.urls', namespace='jobs')),
    path('', include('property.urls', namespace='property')),
    path('', include('reviews.urls', namespace='reviews')),
    path('', include('chat.urls', namespace='chat')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^robots\.txt', include('robots.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)
