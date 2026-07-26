from django.urls import path
from accounts import views

urlpatterns = [
    path("register/", views.farmer_register_view, name="farmer_register"),
    path("login/", views.farmer_login_view, name="farmer_login"),
    path("admin-login/", views.admin_login_view, name="admin_login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("settings/", views.settings_view, name="settings"),
]
