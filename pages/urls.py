from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path('', views.home, name='home'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('cookie/', views.cookie, name='cookie'),
]
