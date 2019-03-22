from django.db import models
from bms_colowell.settings import AUTH_USER_MODEL
from projects.models import InvoiceInfo, ContractsInfo


class SendInvoices(models.Model):
    invoice_number = models.CharField(
        verbose_name="发票号码", max_length=50, null=True, blank=True
    )
    billing_date = models.DateField(
        verbose_name="开票日期", null=True, blank=True
    )
    invoice_send_date = models.DateField(
        verbose_name="寄出日期", null=True, blank=True
    )
    tracking_number = models.CharField(
        verbose_name="快递单号", max_length=25, null=True, blank=True
    )
    ele_invoice = models.FileField(
        verbose_name="电子发票", upload_to="#", max_length=100, null=True,
        blank=True
    )
    fill_date = models.DateField(
        verbose_name="填写日期", auto_now=True
    )
    invoice_id = models.OneToOneField(
        InvoiceInfo, verbose_name="发票编号", on_delete=models.CASCADE
    )
    fill_name = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="填写人", on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    send_flag = models.BooleanField(
        verbose_name="是否提交", default=False
    )
    wait_payment = models.FloatField(
        verbose_name="应收金额", null=True, blank=True, default=0
    )
    tax_rate = models.FloatField(
        verbose_name="税率", null=True, blank=True
    )

    class Meta:
        verbose_name = verbose_name_plural = "发票信息"
        ordering = ["billing_date"]

    def __str__(self):
        return '发票编号{}'.format(self.invoice_id)


class PaymentInfo(models.Model):
    """到款信息"""

    payment_number = models.CharField(
        verbose_name="到款编号", max_length=14, unique=True, null=True, blank=True
    )
    receive_value = models.FloatField(
        verbose_name="到账金额", null=True, blank=True
    )
    receive_date = models.DateField(
        verbose_name="到账时间", null=True, blank=True
    )
    wait_invoices = models.FloatField(
        verbose_name="待开票额", null=True, blank=True, default=0
    )
    send_invoice = models.ManyToManyField(
        SendInvoices, verbose_name="发票编号", blank=True
    )
    contract_number = models.ForeignKey(
        ContractsInfo, verbose_name="合同号", on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    flag = models.BooleanField(
        verbose_name="是否提交", default=False
    )

    class Meta:
        verbose_name = verbose_name_plural = "到款信息"

    def __str__(self):
        return self.payment_number


class TradingRecord(models.Model):
    send_invoices_id = models.ForeignKey(
        SendInvoices, verbose_name="发票编号", on_delete=models.CASCADE,
        null=True, blank=True
    )
    payment_info_id = models.ForeignKey(
        PaymentInfo, verbose_name="到款编号", on_delete=models.CASCADE,
        null=True, blank=True
    )
    transaction_amount = models.FloatField(
        verbose_name="交易金额", null=True, blank=True, default=0
    )
    transaction_date = models.DateField(
        verbose_name="交易时间", auto_now=True
    )

    class Meta:
        verbose_name = verbose_name_plural = "交易记录"

    def __str__(self):
        return '交易编号{}'.format(self.id)
