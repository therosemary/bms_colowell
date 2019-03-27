import os

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.html import format_html


BmsUserModel = get_user_model()


def upload_to_report(obj, filename):
    return os.path.join("lz_reports", filename)


def upload_to_zipped(obj, filename):
    return os.path.join("zipped_files", filename)


class Batches(models.Model):
    batch_code = models.CharField(
        verbose_name="批次号", max_length=18, primary_key=True
    )
    create_at = models.DateField(
        verbose_name="入库于", null=True, blank=True, default=timezone.now
    )

    class Meta:
        ordering = ["-create_at"]
        verbose_name = verbose_name_plural = "批次记录"

    def __str__(self):
        return "%s" % self.batch_code


class LzProducts(models.Model):
    barcode = models.CharField(
        verbose_name="常易舒编号", max_length=18, primary_key=True,
    )
    sample_code = models.CharField(
        verbose_name="样本编号", max_length=18, null=True, blank=True,
    )
    risk_state = models.CharField(
        verbose_name="风险水平", max_length=18, null=True, blank=True,
        help_text="请填写【高风险】或者【低风险】",
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
    batch_code = models.ForeignKey(
        Batches, verbose_name="批次号", on_delete=models.SET_NULL, null=True,
    )
    
    class Meta:
        ordering = ["-received_date"]
        verbose_name = verbose_name_plural = "LZ样品"
    
    def __str__(self):
        return "%s" % self.barcode

    def report_download(self):
        if self.pdf_upload and hasattr(self.pdf_upload, 'url'):
            return format_html(
                '<a href="{}"><b>下载</b></a>', self.pdf_upload.url
            )
        else:
            return "-"
    report_download.short_description = "报告下载"


class BatchDownloadRecords(models.Model):
    serial_number = models.CharField(
        verbose_name="记录流水号", max_length=18, primary_key=True,
    )
    download_by = models.ForeignKey(
        BmsUserModel, verbose_name="下载人", on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name="创建时间", null=True, blank=True, default=timezone.now
    )
    file_counts = models.SmallIntegerField(
        verbose_name="文件数量", null=True, blank=True,
    )
    zipped_file = models.FileField(
        verbose_name="压缩文件", null=True, blank=True,
        upload_to=upload_to_zipped,
    )
    download_uri = models.URLField(
        verbose_name="下载链接", null=True, blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = verbose_name_plural = "批量下载记录"
    
    def __str__(self):
        return "{}".format(self.serial_number)
