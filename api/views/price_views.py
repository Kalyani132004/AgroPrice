"""DRF API views — Price endpoints (/api/v1/prices/...)."""
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils.regex_validators import ValidationError, is_safe_search_query
from prices.services.csv_import_export import CSVImportExportService
from prices.services.price_service import PriceService


class TodayPricesAPIView(APIView):
    """GET /api/v1/prices/today/ — today's price for every crop."""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        service = PriceService()
        return Response({"results": service.today_prices()})


class PriceHistoryAPIView(APIView):
    """GET /api/v1/prices/history/?crop=Wheat&days=30"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        crop_name = request.query_params.get("crop", "").strip()
        days = int(request.query_params.get("days", 30))

        if not crop_name or not is_safe_search_query(crop_name):
            return Response({"error": "A valid `crop` query param is required."}, status=status.HTTP_400_BAD_REQUEST)

        service = PriceService()
        history = service.history(crop_name, days=days)
        stats = service.thirty_day_stats(crop_name)
        return Response({"crop": crop_name, "history": history, "stats": stats})


class PriceSearchAPIView(APIView):
    """GET /api/v1/prices/search/?q=wheat — live search used by navbar search bar."""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        if not query or not is_safe_search_query(query):
            return Response({"results": []})

        from crops.services.crop_service import CropService
        crop_service = CropService()
        matches = crop_service.search(query)
        return Response({"results": [{"id": c.id, "name": c.name, "category": c.category} for c in matches]})


class CompareMarketsAPIView(APIView):
    """GET /api/v1/prices/compare/?crop=Wheat"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        crop_name = request.query_params.get("crop", "").strip()
        if not crop_name:
            return Response({"error": "A `crop` query param is required."}, status=status.HTTP_400_BAD_REQUEST)
        service = PriceService()
        return Response({"crop": crop_name, "markets": service.compare_markets(crop_name)})


class CSVUploadAPIView(APIView):
    """POST /api/v1/prices/upload-csv/ — admin bulk price upload."""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        if not request.user.is_staff:
            return Response({"error": "Admin privileges required."}, status=status.HTTP_403_FORBIDDEN)

        file_obj = request.FILES.get("csv_file")
        if not file_obj:
            return Response({"error": "No file uploaded (expected `csv_file`)."}, status=status.HTTP_400_BAD_REQUEST)

        service = CSVImportExportService()
        result = service.import_prices(file_obj)
        return Response({
            "success_count": result.success_count,
            "errors": result.error_rows,
        }, status=status.HTTP_200_OK)
