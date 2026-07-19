from django.urls import path

from api.views.analytics_views import ProfitCalculatorAPIView, TrendAnalysisAPIView
from api.views.crop_views import CropDetailAPIView, CropListAPIView
from api.views.price_views import (
    CompareMarketsAPIView, CSVUploadAPIView, PriceHistoryAPIView,
    PriceSearchAPIView, TodayPricesAPIView,
)
from api.views.watchlist_views import AdvisorRecommendationAPIView, WatchlistAPIView

urlpatterns = [
    # Crops
    path("crops/", CropListAPIView.as_view(), name="crop_list_api"),
    path("crops/<str:crop_id>/", CropDetailAPIView.as_view(), name="crop_detail_api"),

    # Prices
    path("prices/today/", TodayPricesAPIView.as_view(), name="today_prices_api"),
    path("prices/history/", PriceHistoryAPIView.as_view(), name="price_history_api"),
    path("prices/search/", PriceSearchAPIView.as_view(), name="price_search_api"),
    path("prices/compare/", CompareMarketsAPIView.as_view(), name="compare_markets_api"),
    path("prices/upload-csv/", CSVUploadAPIView.as_view(), name="csv_upload_api"),

    # Analytics
    path("analytics/trend/", TrendAnalysisAPIView.as_view(), name="trend_analysis_api"),
    path("analytics/profit/", ProfitCalculatorAPIView.as_view(), name="profit_calculator_api"),

    # Watchlist + Smart Advisor
    path("watchlist/", WatchlistAPIView.as_view(), name="watchlist_api"),
    path("watchlist/advisor/", AdvisorRecommendationAPIView.as_view(), name="advisor_api"),
]
