from rest_framework.routers import DefaultRouter

from .views import CommodityViewSet

router = DefaultRouter()
router.register(r"commodities", CommodityViewSet, basename="commodity")
urlpatterns = router.urls
