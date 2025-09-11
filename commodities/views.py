from rest_framework import viewsets

from .models import Commodity, CommodityPriceHistory
from .serializers import CommodityPriceHistorySerializer, CommoditySerializer


class CommodityViewSet(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer


class CommodityPriceViewSet(viewsets.ModelViewSet):
    queryset = CommodityPriceHistory.objects.all()
    serializer_class = CommodityPriceHistorySerializer

    def get_queryset(self):
        # filter by commodity symbol
        symbol = self.request.query_params.get("symbol", None)
        if symbol is not None:
            return CommodityPriceHistory.objects.filter(commodity__symbol=symbol)
        return CommodityPriceHistory.objects.all()
