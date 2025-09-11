from rest_framework import serializers

from .models import Commodity, CommodityPriceHistory


class CommodityPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommodityPriceHistory
        fields = "__all__"
        read_only_fields = ["date", "open", "high", "low", "close", "volume"]


class CommoditySerializer(serializers.ModelSerializer):
    latest_price_history = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Commodity
        fields = [
            "id",
            "name",
            "symbol",
            "description",
            "unit",
            "commodity_type",
            "price",
            "updated_at",
            "latest_price_history",
        ]

    def get_latest_price_history(self, obj):
        latest = obj.price_history.first()
        if latest:
            return CommodityPriceHistorySerializer(latest).data
        return None

    def get_price(self, obj):
        latest = obj.price_history.order_by("-date").first()
        return latest.close if latest else None
