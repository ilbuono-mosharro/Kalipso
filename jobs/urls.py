from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path('add/announcement/job/<uuid:category_id>/<uuid:subcat_id>/', views.add_announcement_job,
         name="add_announcement_job"),
    path('update/announcement/job/<uuid:ann_id>/', views.update_announcement_job,
         name="update_announcement_job"),
]
