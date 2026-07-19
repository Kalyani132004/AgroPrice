from django.urls import path
from analytics import views

urlpatterns = [
    path("trends/", views.trend_analysis_view, name="trend_analysis"),
    path("calculator/", views.revenue_calculator_view, name="revenue_calculator"),
]
