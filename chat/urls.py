from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('contact/seller/<slug:ann_id>/', views.contact_seller, name="contact_seller"),
    path('converstions/all/', views.conversations, name="conversations"),
    path('converstion/<uuid:conv_id>/', views.get_conversation, name="get_conversation"),
]
