from django.db import models
from bms_colowell.settings import AUTH_USER_MODEL


class Intentions(models.Model):
    intention_id = models.AutoField(
        verbose_name="编号", primary_key=True
    )
    intention_client = models.CharField(
        verbose_name="意向客户", max_length=100, null=True, blank=True
    )
    contact_number = models.CharField(
        verbose_name="联系电话", max_length=20, null=True, blank=True
    )
    items = models.TextField(
        verbose_name="事项", null=True, blank=True
    )
    # fill_name = models.CharField(
    #     verbose_name="填写人姓名", max_length=20, null=True, blank=True
    # )
    fill_name = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="填写人", on_delete=models.SET_NULL,
        null=True, blank=True
    )
    fill_date = models.DateField(
        verbose_name="填写日期", auto_now_add=True
    )

    class Meta:
        verbose_name = verbose_name_plural = "意向池"
        ordering = ["fill_date"]

    def __str__(self):
        return "%s" % self.intention_id
