import re
from django.db import models
from django.core.exceptions import ValidationError


def barcode_validators(value):
    if not re.match(r'CYS\d{9,10}', str(value)):
        raise ValidationError(
            '%(value)s不符合编码规则', params={'value': value},
        )


class Products(models.Model):
    WAY_CHOICES = (
        ('SAL', u'售出'),
        ('FRE', u'赠送'),
        ('OTH', u'其它'),
    )
    barcode = models.CharField(
        verbose_name="产品条码", max_length=18, primary_key=True,
        validators=[barcode_validators],
        help_text="产品条形码为CYS前缀，后面接9~10位数字，其余皆为非法条形码",
    )
    is_approved = models.BooleanField(
        verbose_name="是否有效", default=True,
    )
    is_sold_out = models.BooleanField(
        verbose_name="是否售出", default=False,
    )
    is_bound = models.BooleanField(
        verbose_name="是否绑定", default=False,
    )
    add_date = models.DateTimeField(
        verbose_name="增加日期", null=True, blank=True,
    )
    sold_date = models.DateTimeField(
        verbose_name="售出日期", null=True, blank=True,
    )
    sold_to = models.CharField(
        verbose_name="售出至？", max_length=128, null=True, blank=True,
    )
    sold_way = models.CharField(
        verbose_name="出库方式", max_length=3, null=True, blank=True,
        default="SAL", choices=WAY_CHOICES,
    )
    operator = models.CharField(
        verbose_name="操作人员", max_length=32, null=True, blank=True
    )
    
    class Meta:
        ordering = ["-add_date"]
        verbose_name = verbose_name_plural = "产品库存"
    
    def __str__(self):
        return "%s" % self.barcode
