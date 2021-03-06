from django.db import models
from bms_colowell.settings import AUTH_USER_MODEL


class Intentions(models.Model):
    salesman = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="销售", on_delete=models.SET_NULL,
        null=True, blank=True
    )
    intention_client = models.CharField(
        verbose_name="意向名称", max_length=100, null=True, blank=True,
        help_text="需填写信息：意向单位、代理区域、代理产品及代理级别"
    )
    contact_name = models.CharField(
        verbose_name="联系人姓名", max_length=50, null=True, blank=True
    )
    contact_number = models.CharField(
        verbose_name="电话（或微信）", max_length=50, null=True, blank=True
    )
    intention_progress = models.TextField(
        verbose_name="意向进展", null=True, blank=True
    )
    remark = models.TextField(
        verbose_name="备注", null=True, blank=True
    )
    fill_date = models.DateField(
        verbose_name="填写日期", auto_now_add=True
    )

    class Meta:
        verbose_name = verbose_name_plural = "意向池"
        ordering = ["fill_date"]

    def __str__(self):
        return "意向{}".format(self.id)
