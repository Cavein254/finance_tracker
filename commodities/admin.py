from django.contrib import admin

from .models import Commodity, CommodityPriceHistory


class CommodityPriceHistoryInline(admin.TabularInline):
    model = CommodityPriceHistory
    extra = 1
    readonly_fields = ("date", "open", "high", "low", "close", "volume")
    can_delete = False


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ("name", "symbol", "commodity_type", "price", "updated_at")
    search_fields = ("name", "symbol")
    list_filter = ("commodity_type",)
    ordering = ("name",)
    inlines = [CommodityPriceHistoryInline]


@admin.register(CommodityPriceHistory)
class CommodityPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("commodity", "date", "open", "high", "low", "close", "volume")
    search_fields = ("commodity__name", "commodity__symbol")
    list_filter = ("commodity", "date")
    ordering = ("-date",)
