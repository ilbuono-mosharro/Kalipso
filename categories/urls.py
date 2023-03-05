from django.urls import path
from . import views

app_name = "categories"

urlpatterns = [
    path('choose-the-category/', views.categories_list, name="categories_list"),
]
