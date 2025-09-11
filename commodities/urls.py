from rest_framework.routers import DefaultRouter

from .views import CommodityPriceViewSet, CommodityViewSet

router = DefaultRouter()
router.register(r"commodities", CommodityViewSet, basename="commodity")
router.register(r"prices", CommodityPriceViewSet, basename="commodity-price")
urlpatterns = router.urls
