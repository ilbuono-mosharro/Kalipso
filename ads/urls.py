from django.urls import path
from . import views

app_name = "ads"

urlpatterns = [
    path('announcements/', views.announcements,
         name="announcements"),
    path('announcements/<slug:category_slug>/', views.categories_and_sub,
         name="announcements_by_category"),
    path('announcements/<slug:category_slug>/<slug:sabcategory_slug>/', views.categories_and_sub,
         name="announcements_by_subcategory"),
    path('announcements/add/to/wishlist/', views.ann_wishlist,
         name="ann_wishlist"),
    path('announcements/add/to/wishlist/<uuid:announcement_id>/', views.ann_wishlist,
         name="ann_wishlist_detail"),
    path('announcement/<slug:slug>/detail/', views.announcement_detail,
         name="announcement_detail"),
    path('add/announcement/<uuid:category_id>/<uuid:subcat_id>/', views.add_standard_announcement,
         name="add_standard_announcement"),
    path('update/announcement/<uuid:ann_id>/', views.update_standard_announcement,
         name="update_standard_announcement"),
    path('delete/announcement/<uuid:ann_id>/', views.delete_announcement,
         name="delete_announcement"),
    path('change-status/announcement/<uuid:ann_id>/', views.change_status_announcement,
         name="change_status_announcement"),
    path('add/images/announcement/<uuid:ad_id>/', views.add_image_announcement,
         name="add_image_announcement"),
    path('modify/images/announcement/<uuid:image_id>/', views.modify_image_announcement,
         name="modify_image_announcement"),
    path('delete/images/announcement/<uuid:image_id>/', views.delete_image_announcement,
         name="delete_image_announcement"),
]
