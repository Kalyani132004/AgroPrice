
# DRF API Views  REST API endpoints for trend analysis and profit calculation.

from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.domain.profit_calculator import ProfitCalculator
from analytics.domain.trend_analyzer import TrendAnalyzer
from api.serializers.analytics_serializers import (
    ProfitRequestSerializer, ProfitResultSerializer, TrendSummarySerializer,
)
from core.utils.regex_validators import is_safe_search_query
from prices.services.price_service import PriceService


class TrendAnalysisAPIView(APIView):
    """GET /api/v1/analytics/trend/?crop=Wheat&days=30"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        crop_name = request.query_params.get("crop", "").strip()
        days = int(request.query_params.get("days", 30))

        if not crop_name or not is_safe_search_query(crop_name):
            return Response({"error": "A valid `crop` query param is required."}, status=status.HTTP_400_BAD_REQUEST)

        service = PriceService()
        history = service.history(crop_name, days=days)
        analyzer = TrendAnalyzer(history)
        summary = analyzer.summary()

        return Response({
            "crop": crop_name,
            "summary": TrendSummarySerializer(summary).data,
            "chart": {
                "labels": [h["date_display"].split(",")[0] for h in history],
                "prices": [h["price"] for h in history],
            },
        })


class ProfitCalculatorAPIView(APIView):
    """POST /api/v1/analytics/profit/ — body: quantity, selling_price_per_unit, costs..."""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = ProfitRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        v = serializer.validated_data

        calculator = ProfitCalculator(
            quantity=v["quantity"],
            selling_price_per_unit=v["selling_price_per_unit"],
            cultivation_cost=v.get("cultivation_cost", 0),
            transport_cost=v.get("transport_cost", 0),
            labour_cost=v.get("labour_cost", 0),
            misc_cost=v.get("misc_cost", 0),
        )
        result = calculator.summary()
        return Response(ProfitResultSerializer(result).data, status=status.HTTP_200_OK)
