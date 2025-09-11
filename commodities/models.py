from django.db import models


class Commodity(models.Model):
    COMMODITY_TYPES = [
        ("AGRICULTURE", "Agriculture"),
        ("ENERGY", "Energy"),
        ("METAL", "Metal"),
        ("LIVESTOCK", "Livestock"),
        ("ALTERNATIVE", "Alternative Asset"),
    ]

    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=50, default="unit")
    commodity_type = models.CharField(
        max_length=50, choices=COMMODITY_TYPES, default="ALTERNATIVE"
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    class Meta:
        verbose_name = "Commodity"
        verbose_name_plural = "Commodities"
        ordering = ["name"]


class CommodityPriceHistory(models.Model):
    commodity = models.ForeignKey(
        Commodity, on_delete=models.CASCADE, related_name="price_history"
    )
    date = models.DateField()
    open = models.DecimalField(max_digits=15, decimal_places=2)
    high = models.DecimalField(max_digits=15, decimal_places=2)
    low = models.DecimalField(max_digits=15, decimal_places=2)
    close = models.DecimalField(max_digits=15, decimal_places=2)
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ("commodity", "date")
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.commodity.price = self.close
        self.commodity.save(update_fields=["price", "updated_at"])

    def __str__(self):
        return f"{self.commodity.name} - {self.date}: {self.price}"
