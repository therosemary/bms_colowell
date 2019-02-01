from django.db import models
from products.models import Products


class Suggestions(models.Model):
    FACTOR_CHOICES = (
        (1, "建议参考因子1"),
        (2, "建议参考因子2"),
        (3, "建议参考因子3"),
    )
    product = models.OneToOneField(
        Products, verbose_name="样品条码", on_delete=models.CASCADE
    )
    factor_1 = models.CharField(
        verbose_name="参考因子1", max_length=2, choices=FACTOR_CHOICES
    )
    factor_2 = models.CharField(
        verbose_name="参考因子2", max_length=2, choices=FACTOR_CHOICES
    )
    factor_3 = models.CharField(
        verbose_name="参考因子3", max_length=2, choices=FACTOR_CHOICES
    )

    