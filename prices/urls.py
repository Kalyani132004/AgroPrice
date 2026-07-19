from django.urls import path
from prices import views

urlpatterns = [
    path("today/", views.today_prices_view, name="today_prices"),
    path("history/", views.historical_prices_view, name="historical_prices"),
    path("compare/", views.compare_markets_view, name="compare_markets"),
    path("upload-csv/", views.upload_csv_view, name="upload_csv"),
    path("download-csv/", views.download_csv_view, name="download_csv"),
    path("add/", views.add_price_view, name="add_price"),
]
