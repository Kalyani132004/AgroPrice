# from django.urls import path
# from dashboard import views

# urlpatterns = [
#     path("farmer/", views.farmer_dashboard_view, name="farmer_dashboard"),
#     path("admin/", views.admin_dashboard_view, name="admin_dashboard"),
#     path("reports/", views.reports_view, name="reports"),
#     path("messages/", views.contact_messages_view, name="contact_messages"),
# ]

from django.urls import path
from dashboard import views

urlpatterns = [
    path("farmer/", views.farmer_dashboard_view, name="farmer_dashboard"),
    path("admin/", views.admin_dashboard_view, name="admin_dashboard"),
    path("reports/", views.reports_view, name="reports"),
    path("messages/", views.contact_messages_view, name="contact_messages"),
    path("messages/read/<str:message_id>/", views.mark_message_read, name="mark_message_read",),
    path("messages/delete/<str:message_id>/", views.delete_message, name="delete_message",), 
    path("registered-farmers/", views.registered_farmers, name="registered_farmers"),
    path("registered-farmers/delete/<int:auth_user_id>/", views.delete_farmer, name="delete_farmer"),
]