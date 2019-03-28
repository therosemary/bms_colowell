import os
import re

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from bms_colowell.settings import AUTH_USER_MODEL


def barcode_validators(value):
    if not re.match(r'CYS\d{9,10}', str(value)):
        raise ValidationError(
            '%(value)s不符合编码规则', params={'value': value},
        )


def upload_to(obj, filename):
    return os.path.join("products", filename)


class Deliveries(models.Model):
    """Deliveries management."""
    
    LIMIT_CHOICES_TO = {
        "is_staff": True,
        "is_superuser": False,
    }
    serial_number = models.CharField(
        verbose_name="流水号", max_length=20, primary_key=True
    )
    salesman = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="业务员", on_delete=models.SET_NULL,
        null=True, limit_choices_to=LIMIT_CHOICES_TO,
    )
    customer = models.CharField(
        verbose_name="客户", max_length=256, null=True, blank=True,
    )
    is_submit = models.BooleanField(
        verbose_name='提交', default=False
    )
    add_date = models.DateField(
        verbose_name="发货日期", null=True, blank=True, default=timezone.now
    )
    
    def __str__(self):
        return "%s" % self.serial_number
    
    class Meta:
        verbose_name = verbose_name_plural = "盒子发货记录"


class Products(models.Model):
    WAY_CHOICES = (
        ('SAL', u'售出'),
        ('FRE', u'赠送'),
        ('OTH', u'其它'),
    )
    barcode = models.CharField(
        verbose_name="盒子条码", max_length=18, primary_key=True,
        validators=[barcode_validators],
        help_text="盒子条码为CYS前缀，后面接9~10位数字，其余皆为非法条形码",
    )
    barcode_img = models.ImageField(
        verbose_name="条码图片", upload_to=upload_to,
        default="products/CYS000000000.png"
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
        verbose_name="增加日期", auto_now_add=True
    )
    sold_date = models.DateTimeField(
        verbose_name="出库日期", null=True, blank=True,
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
    serial_number = models.ForeignKey(
        Deliveries, verbose_name="发货号", on_delete=models.SET_NULL, null=True
    )
    
    class Meta:
        ordering = ["-add_date"]
        verbose_name = verbose_name_plural = "盒子"
    
    def __str__(self):
        return "%s" % self.barcode
