""" serializers for price records and price creation requests. """

from rest_framework import serializers


class PriceRecordSerializer(serializers.Serializer):
    crop_name = serializers.CharField()
    market = serializers.CharField()
    price = serializers.FloatField()
    quality = serializers.CharField()
    date_display = serializers.CharField(required=False)


class PriceCreateSerializer(serializers.Serializer):
    crop_name = serializers.CharField(max_length=50)
    market = serializers.CharField(max_length=50)
    price = serializers.CharField()
    quality = serializers.CharField(max_length=20)
