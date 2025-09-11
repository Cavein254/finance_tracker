import logging

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Commodity, CommodityPriceHistory
from .serializers import CommodityPriceHistorySerializer, CommoditySerializer
from .tasks import fetch_commodity_history
from .utils import fetch_yfinance_data

logger = logging.getLogger(__name__)


# TODO: Add cahche, filtering, pagination, and search functionality
class CommodityViewSet(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    permission_classes = [AllowAny]


class CommodityPriceViewSet(viewsets.ModelViewSet):
    queryset = CommodityPriceHistory.objects.all()
    serializer_class = CommodityPriceHistorySerializer
    permission_classes = [AllowAny]
    lookup_field = "symbol"

    @action(detail=True, methods=["get"])
    def prices(self, request, symbol=None):
        """
        Retrieve commodity data either from the database
        or internet
        """
        try:
            commodity = Commodity.objects.get(symbol=symbol.upper())
            serializer = CommoditySerializer(commodity)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except commodity.DoesNotExist:
            # get from the internet
            logger.info(f"Fetching prices for symbol: {symbol}")
            data = fetch_yfinance_data(symbol)
            if data.get("status") is False:
                return Response(
                    {"error": data.get("message")},
                    status=status.HTTP_404_NOT_FOUND,
                )
            # enqueue background task for 5 years
            fetch_commodity_history.delay(symbol)
            return Response(data.get("data"), status=status.HTTP_200_OK)
