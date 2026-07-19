"""DRF API views — Watchlist + Smart Advisor endpoints (/api/v1/watchlist/...)."""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services.watchlist_service import WatchlistService
from analytics.services.advisor_service import AdvisorService
from api.serializers.watchlist_serializers import WatchlistItemSerializer, WatchlistToggleSerializer
from core.utils.regex_validators import is_safe_search_query


class WatchlistAPIView(APIView):
    """
    GET  /api/v1/watchlist/            -> current farmer's enriched watchlist
    POST /api/v1/watchlist/            -> body: {crop_name, alert_threshold?} toggles watchlist membership
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = WatchlistService()
        items = service.get_watchlist_with_prices(request.user.id)
        return Response({"results": WatchlistItemSerializer(items, many=True).data})

    def post(self, request):
        serializer = WatchlistToggleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        crop_name = serializer.validated_data["crop_name"]

        if not is_safe_search_query(crop_name):
            return Response({"error": "Invalid crop name."}, status=status.HTTP_400_BAD_REQUEST)

        service = WatchlistService()
        now_watchlisted = service.toggle(
            request.user.id, crop_name, serializer.validated_data.get("alert_threshold")
        )
        return Response({"crop_name": crop_name, "watchlisted": now_watchlisted}, status=status.HTTP_200_OK)


class AdvisorRecommendationAPIView(APIView):
    """GET /api/v1/watchlist/advisor/?crop=Wheat — Smart Sell/Hold recommendation."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        crop_name = request.query_params.get("crop", "").strip()
        if not crop_name or not is_safe_search_query(crop_name):
            return Response({"error": "A valid `crop` query param is required."}, status=status.HTTP_400_BAD_REQUEST)

        result = AdvisorService().recommend(crop_name, days=30)
        return Response({"crop": crop_name, "recommendation": result})
