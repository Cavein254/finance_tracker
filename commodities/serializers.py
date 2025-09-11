from rest_framework import serializers

from .models import Commodity


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ["id", "name", "description", "price", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
