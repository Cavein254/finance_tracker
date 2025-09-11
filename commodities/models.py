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
    current_price = models.DecimalField(max_digits=15, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    class Meta:
        verbose_name = "Commodity"
        verbose_name_plural = "Commodities"
        ordering = ["name"]
