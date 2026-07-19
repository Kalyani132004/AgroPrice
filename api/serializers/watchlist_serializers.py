# Serializers for the Watchlist API

from rest_framework import serializers


class WatchlistItemSerializer(serializers.Serializer):
    crop_name = serializers.CharField()
    crop_id = serializers.CharField(allow_null=True, required=False)
    alert_threshold = serializers.FloatField(allow_null=True, required=False)
    latest_price = serializers.FloatField(allow_null=True, required=False)
    market = serializers.CharField(allow_null=True, required=False)
    alert_triggered = serializers.BooleanField()


class WatchlistToggleSerializer(serializers.Serializer):
    crop_name = serializers.CharField(max_length=50)
    alert_threshold = serializers.FloatField(required=False, allow_null=True)
