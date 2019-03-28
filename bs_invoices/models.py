from django.db import models

from bms_colowell.settings import AUTH_USER_MODEL
from projects.models import ContractsInfo


class BusinessRecord(models.Model):
    """业务流表"""

    record_number = models.CharField(
        verbose_name="业务流编号", max_length=18
    )
    contract_number = models.ForeignKey(
        ContractsInfo, verbose_name="合同编号", on_delete=models.SET_NULL,
        null=True, blank=True
    )

    class Meta:
        verbose_name = verbose_name_plural = "业务流"

    def __str__(self):
        return '业务流编号{}'.format(self.record_number)


class Payment(models.Model):
    """到款信息"""

    payment_number = models.CharField(
        verbose_name="到款编号", max_length=14, unique=True, null=True,
        blank=True
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
    flag = models.BooleanField(
        verbose_name="是否提交", default=False
    )
    record_number = models.ForeignKey(
        BusinessRecord, verbose_name="业务流编号", on_delete=models.SET_NULL,
        null=True, blank=True
    )

    class Meta:
        verbose_name = verbose_name_plural = "到款信息"

    def __str__(self):
        return self.payment_number


class Invoices(models.Model):
    COST_TYPE_CHOICE = (
        ('BOX', u'盒子'),
        ('DET', u'检测'),
        ('ALL', u'全套'),
    )
    IVOICE_ISSUING_CHOICE = (
        ('shry', u'上海锐翌'),
        ('hzth', u'杭州拓宏'),
        ('hzry', u'杭州锐翌'),
        ('sdry', u'山东锐翌'),
    )
    INVOICE_TYPE = (
        ('pp', u'普票'),
        ('zp', u'专票'),
    )
    APPROVE_CHOICE = (
        ('tg', u'审核通过'),
        ('ds', u'待审核'),
        ('btg', u'不通过'),
    )
    invoice_id = models.CharField(
        verbose_name="发票编号", max_length=18, unique=True,
    )
    contract_id = models.ForeignKey(
        ContractsInfo, verbose_name="合同号", on_delete=models.SET_NULL,
        null=True, blank=True
    )
    salesman = models.CharField(
        verbose_name="业务员", max_length=50, null=True, blank=True
    )
    invoice_type = models.CharField(
        verbose_name="开票类型", choices=INVOICE_TYPE, max_length=2, default='pp'
    )
    invoice_issuing = models.CharField(
        verbose_name="开票单位", choices=IVOICE_ISSUING_CHOICE,
        max_length=4, default="hzry"
    )
    invoice_title = models.CharField(
        verbose_name="抬头", max_length=100, null=True, blank=True
    )
    tariff_item = models.CharField(
        verbose_name="税号", max_length=200, null=True, blank=True
    )
    send_address = models.CharField(
        verbose_name="对方地址", max_length=150, null=True, blank=True
    )
    address_phone = models.CharField(
        verbose_name="电话", max_length=20, null=True, blank=True
    )
    opening_bank = models.CharField(
        verbose_name="开户行", max_length=150, null=True, blank=True
    )
    bank_account_number = models.CharField(
        verbose_name="账号", max_length=50, null=True, blank=True
    )
    invoice_value = models.FloatField(
        verbose_name="开票金额", null=True, blank=True
    )
    invoice_content = models.CharField(
        verbose_name="开票内容", max_length=150, null=True, blank=True
    )
    remark = models.TextField(
        verbose_name="备注", null=True, blank=True
    )
    apply_name = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="申请人", on_delete=models.SET_NULL,
        null=True, blank=True
    )
    flag = models.BooleanField(
        verbose_name="提交开票", default=False
    )
    invoice_fill_date = models.DateField(
        verbose_name="填写日期", auto_now_add=True
    )
    approve_flag = models.CharField(
        verbose_name="审核状态", max_length=3, choices=APPROVE_CHOICE, null=True,
        blank=True, default='ds'
    )
    approve_submit_flag = models.BooleanField(
        verbose_name="提交审核", default=False
    )

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
        verbose_name="电子发票", upload_to="ele_invoice", max_length=100, null=True,
        blank=True
    )
    send_fill_date = models.DateField(
        verbose_name="填写日期", auto_now=True
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
    record_number = models.ForeignKey(
        BusinessRecord, verbose_name="业务流编号", on_delete=models.SET_NULL,
        null=True, blank=True,
    )

    def __str__(self):
        return "{}".format(self.invoice_number)

    class Meta:
        verbose_name = verbose_name_plural = "开票信息"
        ordering = ['invoice_fill_date']

    @staticmethod
    def autocomplete_search_fields():
        return 'salesman',

