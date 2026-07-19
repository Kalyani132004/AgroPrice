"""DRF API views — Crop endpoints (/api/v1/crops/...)."""
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.crop_serializers import CropSerializer, CropCreateSerializer
from core.utils.regex_validators import ValidationError, is_safe_search_query
from crops.services.crop_service import CropService


class CropListAPIView(APIView):
    """GET: list/search crops. POST: create a crop (admin only)."""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        service = CropService()
        query = request.query_params.get("q", "").strip()

        if query and not is_safe_search_query(query):
            return Response({"error": "Invalid search query."}, status=status.HTTP_400_BAD_REQUEST)

        crops = service.search(query) if query else service.list_all()
        data = [c.__dict__ for c in crops]
        serializer = CropSerializer(data, many=True)
        return Response({"count": len(data), "results": serializer.data})

    def post(self, request):
        if not request.user.is_staff:
            return Response({"error": "Admin privileges required."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CropCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = CropService()
        try:
            crop_id = service.add_crop(
                name=serializer.validated_data["name"],
                category=serializer.validated_data["category"],
                unit=serializer.validated_data.get("unit", "Quintal"),
                quality_grades=serializer.validated_data.get("quality_grades", ["FAQ"]),
                description=serializer.validated_data.get("description", ""),
            )
            return Response({"id": crop_id, "message": "Crop created."}, status=status.HTTP_201_CREATED)
        except ValidationError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class CropDetailAPIView(APIView):
    """GET: crop details. DELETE: remove a crop (admin only)."""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, crop_id):
        service = CropService()
        crop = service.get_by_id(crop_id)
        if not crop:
            return Response({"error": "Crop not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(CropSerializer(crop.__dict__).data)

    def delete(self, request, crop_id):
        if not request.user.is_staff:
            return Response({"error": "Admin privileges required."}, status=status.HTTP_403_FORBIDDEN)
        service = CropService()
        try:
            deleted = service.delete_crop(crop_id)
            if not deleted:
                return Response({"error": "Crop not found."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Crop deleted."}, status=status.HTTP_200_OK)
        except ValidationError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
