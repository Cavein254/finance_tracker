from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommodityPriceViewSet, CommodityViewSet

router = DefaultRouter()
router.register(r"", CommodityViewSet, basename="commodity")
urlpatterns = [
    # This automatically includes the standard CRUD endpoints
    path("", include(router.urls)),
    # This line adds a custom route for your prices method
    path(
        "<str:symbol>/prices/",
        CommodityPriceViewSet.as_view({"get": "prices"}),
    ),
]
