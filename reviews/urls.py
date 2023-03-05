from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path('dashboard/review/update/<uuid:review_id>/', views.modify_review, name='modify_review'),
    path('dashboard/review/delete/<uuid:review_id>/', views.delete_review, name='delete_review'),
]
