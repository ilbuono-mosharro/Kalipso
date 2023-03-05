from django.urls import path
from . import views

app_name = "property"

urlpatterns = [
    path('add/announcement/property/<uuid:category_id>/<uuid:subcat_id>/', views.add_announcement_property,
         name="add_announcement_property"),
    path('update/announcement/property/<uuid:ann_id>/', views.update_announcement_property,
         name="update_announcement_property"),
    path('add/announcement/property/aparments/<uuid:category_id>/<uuid:subcat_id>/', views.add_announcement_apartments,
         name="add_announcement_apartments"),
    path('update/announcement/property/aparments/<uuid:ann_id>/', views.update_announcement_apartments,
         name="update_announcement_apartments")
]
