from rest_framework import serializers

from .models import Commodity, CommodityPriceHistory


class CommodityPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommodityPriceHistory
        fields = ["date", "open", "high", "low", "close", "volume"]
        read_only_fields = ["date", "open", "high", "low", "close", "volume"]


class CommoditySerializer(serializers.ModelSerializer):
    price_history = CommodityPriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Commodity
        fields = "__all__"
