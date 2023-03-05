from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-up/info-account-activation/', views.info_account_activation, name='info_account_activation'),
    path('sign-up/confermation-account/<slug:uidb64>/<slug:token>/', views.activate_account, name='activate_account'),
    path('dashboard/accounts/update/profile/', views.update_profile, name='update_profile'),
    path('dashboard/accounts/delete/account/', views.delete_user, name="delete_user"),
    path('dashboard/ads/', views.user_ads, name="user_ads"),
    path('dashboard/wishlist/', views.user_wishlist, name="user_wishlist"),
    path('dashboard/reviews/', views.user_reviews, name="user_reviews"),
    path('dashboard/update/review/<uuid:review_id>/', views.update_review, name="update_review"),
    path('dashboard/delete/review/<uuid:review_id>/', views.delete_review, name="delete_review"),
    path('profile/<str:unique_code>/', views.public_profile, name="public_profile"),
]
