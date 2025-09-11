import logging

import pandas as pd
import yfinance as yt
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Commodity, CommodityPriceHistory
from .serializers import CommodityPriceHistorySerializer, CommoditySerializer

logger = logging.getLogger(__name__)


# TODO: Add cahche, filtering, pagination, and search functionality
class CommodityViewSet(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    lookup_field = "symbol"
    permission_classes = [AllowAny]


class CommodityPriceViewSet(viewsets.ModelViewSet):
    queryset = CommodityPriceHistory.objects.all()
    serializer_class = CommodityPriceHistorySerializer
    permission_classes = [AllowAny]

    def prices(self, request, symbol=None):
        """
        Retrieve 1 year price info
        """
        logger.info(f"Fetching prices for symbol: {symbol}")
        try:
            data = yt.download(
                tickers=symbol,
                period="1y",
                interval="1d",
                group_by="ticker",
                auto_adjust=True,
            )
            print("Data fetched:", data)
            if data.empty:
                return Response(
                    {"error": "No data found"}, status=status.HTTP_404_NOT_FOUND
                )
            else:
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = [
                        "_".join([str(c) for c in col if c]) for col in data.columns
                    ]
                # Reset index so Date becomes a column
                records = data.reset_index().to_dict(orient="records")
                return Response(records)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
