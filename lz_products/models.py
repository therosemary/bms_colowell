import os
from django.db import models
from django.utils import timezone


def upload_to_report(obj, filename):
    return os.path.join("lz_reports", filename)


class LzProducts(models.Model):
    barcode = models.CharField(
        verbose_name="常易舒编号", max_length=18, primary_key=True,
    )
    sample_code = models.CharField(
        verbose_name="样本编号", max_length=18, null=True, blank=True,
    )
    received_date = models.DateField(
        verbose_name="收样日期", null=True, blank=True, default=timezone.now
    )
    test_date = models.DateField(
        verbose_name="检测日期", null=True, blank=True, default=timezone.now
    )
    report_date = models.DateField(
        verbose_name="报告日期", null=True, blank=True, default=timezone.now
    )
    operator = models.CharField(
        verbose_name="操作人员", max_length=32, null=True, blank=True
    )
    pdf_upload = models.FileField(
        verbose_name="报告", null=True, blank=True,
        upload_to=upload_to_report,
    )
    
    class Meta:
        ordering = ["-received_date"]
        verbose_name = verbose_name_plural = "LZ样品"
    
    def __str__(self):
        return "%s" % self.barcode
