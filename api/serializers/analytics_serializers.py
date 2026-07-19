""" Defines serializers for trend analysis and profit calculator data. """
from rest_framework import serializers


class TrendSummarySerializer(serializers.Serializer):
    average = serializers.FloatField()
    highest = serializers.FloatField()
    lowest = serializers.FloatField()
    volatility = serializers.FloatField()
    trend = serializers.CharField()
    change_percent = serializers.FloatField()
    data_points = serializers.IntegerField()


class ProfitRequestSerializer(serializers.Serializer):
    quantity = serializers.FloatField(min_value=0)
    selling_price_per_unit = serializers.FloatField(min_value=0)
    cultivation_cost = serializers.FloatField(min_value=0, required=False, default=0)
    transport_cost = serializers.FloatField(min_value=0, required=False, default=0)
    labour_cost = serializers.FloatField(min_value=0, required=False, default=0)
    misc_cost = serializers.FloatField(min_value=0, required=False, default=0)


class ProfitResultSerializer(serializers.Serializer):
    total_revenue = serializers.FloatField()
    total_cost = serializers.FloatField()
    net_profit = serializers.FloatField()
    profit_margin_percent = serializers.FloatField()
    break_even_price = serializers.FloatField()
    is_profitable = serializers.BooleanField()
