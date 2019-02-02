from django.db import models
from products.models import Products


class Suggestions(models.Model):
    FACTOR_CHOICES = (
        (1, "经常"),
        (2, "偶尔"),
        (3, "从不"),
    )
    product = models.OneToOneField(
        Products, verbose_name="样品条码", on_delete=models.CASCADE
    )
    state_of_smoking = models.CharField(
        verbose_name="抽烟", max_length=2, choices=FACTOR_CHOICES
    )
    state_of_drinking = models.CharField(
        verbose_name="喝酒", max_length=2, choices=FACTOR_CHOICES
    )
    enteroscopy = models.BooleanField(
        verbose_name="肠镜", default=False,
    )
    polyp_or_cancer = models.BooleanField(
        verbose_name="直系肠癌史", default=False,
    )
    state_of_lower_digestive_tract = models.CharField(
        verbose_name="下消化道症状", max_length=512, null=True, blank=True,
    )
    state_of_specified_disease = models.CharField(
        verbose_name="以下其它病史", max_length=512, null=True, blank=True,
    )
    state_of_other_disease = models.CharField(
        verbose_name="其它慢性病史", max_length=512, null=True, blank=True,
    )
    notes = models.TextField(
        verbose_name="备注", null=True, blank=True,
    )
    
    class Meta:
        verbose_name = verbose_name_plural = "健康建议"

    def __str__(self):
        return '盒子申请编号：{}'.format(self.product.barcode)
