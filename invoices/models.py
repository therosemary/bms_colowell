from django.db import models
from projects.models import InvoiceInfo


class SendInvoices(models.Model):
    invoice_number = models.CharField(
        verbose_name="发票号码", max_length=8, null=True, blank=True
    )
    billing_date = models.DateField(
        verbose_name="开票日期", null=True, blank=True
    )
    send_date = models.DateField(
        verbose_name="寄出日期", null=True, blank=True
    )
    tracking_number = models.CharField(
        verbose_name="快递单号", max_length=25, null=True, blank=True
    )
    ele_invoice = models.FileField(
        verbose_name="电子发票", upload_to="#", max_length=100, null=True,
        blank=True
    )
    invoice_flag = models.BooleanField(
        verbose_name="到款标志", default=False, null=True, blank=True
    )
    sender = models.CharField(
        verbose_name="寄件人", max_length=20, null=True, blank=True
    )
    fill_date = models.DateField(
        verbose_name="填写日期", auto_now=True
    )
    invoice_id = models.OneToOneField(
        InvoiceInfo, verbose_name="发票编号", on_delete=models.CASCADE
    )
    fill_name = models.CharField(
        verbose_name="填写人", max_length=20, null=True, blank=True
    )
    flag = models.BooleanField(
        verbose_name="是否提交", default=False
    )

    class Meta:
        verbose_name = verbose_name_plural = "发票信息"
        ordering = ["billing_date"]

    def __str__(self):
        return '%s' % self.invoice_number
