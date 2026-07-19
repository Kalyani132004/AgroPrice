# Defines serializers for crop data and crop creation requests - since Crop lives in MongoDB

from rest_framework import serializers


class CropSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    category = serializers.CharField()
    unit = serializers.CharField()
    quality_grades = serializers.ListField(child=serializers.CharField())
    description = serializers.CharField(allow_blank=True)


class CropCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    category = serializers.CharField(max_length=50)
    unit = serializers.CharField(max_length=20, default="Quintal")
    quality_grades = serializers.ListField(child=serializers.CharField(), required=False)
    description = serializers.CharField(required=False, allow_blank=True)
