from django.urls import path
from crops import views

urlpatterns = [
    path("", views.crop_list_view, name="crop_list"),
    path("manage/", views.manage_crops_view, name="manage_crops"),
    path("<str:crop_id>/", views.crop_detail_view, name="crop_detail"),
    path("<str:crop_id>/watchlist/", views.toggle_watchlist_view, name="toggle_watchlist"),
]
