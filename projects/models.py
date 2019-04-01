from django.db import models

from bms_colowell.settings import AUTH_USER_MODEL
from partners.models import Partners


class ContractsInfo(models.Model):

    CONTRACT_TYPE = (
        ('ZS', u'正式合同'),
        ('YX', u'意向合同'),
    )
    contract_code = models.CharField(
        verbose_name="合同编码", max_length=18, unique=True
    )
    contract_number = models.CharField(
        verbose_name="合同号", max_length=50, unique=True
    )
    client = models.ForeignKey(
        Partners, verbose_name="客户", on_delete=models.SET_NULL, null=True,
        blank=True
    )
    box_price = models.FloatField(
        verbose_name="盒子单价", null=True, blank=True
    )
    detection_price = models.FloatField(
        verbose_name="检测单价", null=True, blank=True
    )
    contract_money = models.FloatField(
        verbose_name="合同金额", null=True, blank=True
    )
    send_date = models.DateField(
        verbose_name="寄出时间", null=True, blank=True
    )
    tracking_number = models.CharField(
        verbose_name="邮件单号", max_length=32, null=True, blank=True
    )
    send_back_date = models.DateField(
        verbose_name="寄回时间", null=True, blank=True
    )
    contract_content = models.FileField(
        verbose_name="合同内容", upload_to="contract", max_length=100, null=True,
        blank=True
    )
    contract_type = models.CharField(
        verbose_name="合同类型", max_length=3, choices=CONTRACT_TYPE,  null=True,
        blank=True
    )
    start_date = models.DateField(
        verbose_name="起始时间", null=True, blank=True
    )
    end_date = models.DateField(
        verbose_name="截止时间", null=True, blank=True
    )
    remark = models.TextField(
        verbose_name="备注", null=True, blank=True
    )
    staff_name = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="业务员", on_delete=models.SET_NULL,
        null=True, blank=True
    )

    class Meta:
        verbose_name = verbose_name_plural = "合同信息"
        ordering = ["send_back_date"]

    def __str__(self):
        return '{}'.format(self.contract_number)
