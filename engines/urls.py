from django.urls import path
from . import views

app_name = "engines"

urlpatterns = [
    path('add/announcement/auto/<uuid:category_id>/<uuid:subcat_id>/', views.add_announcement_auto,
         name="add_announcement_auto"),
    path('update/announcement/auto/<uuid:ann_id>/', views.update_announcement_auto,
         name="update_announcement_auto"),
    path('add/announcement/moto/<uuid:category_id>/<uuid:subcat_id>/', views.add_announcement_moto,
         name="add_announcement_moto"),
    path('update/announcement/moto/<uuid:ann_id>/', views.update_announcement_moto,
         name="update_announcement_moto"),
]
