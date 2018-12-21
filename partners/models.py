from django.db import models
from django.conf import settings


class Partners(models.Model):
    REGION_CHOICES = (
        ("1", u"华中大区"),
        ("2", u"华北大区"),
        ("3", u"西北大区"),
        ("4", u"其它"),
    )
    MODE_CHOICES = (
        ("1", u"省级代理"),
        ("2", u"市级代理"),
        ("3", u"经销商"),
        ("4", u"其它"),
    )
    bms_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="用户",
        on_delete=models.CASCADE,
    )
    code = models.CharField(
        verbose_name="编号", max_length=32, primary_key=True,
    )
    name = models.CharField(
        verbose_name="名称", max_length=32, null=True, blank=True,
    )
    mode = models.CharField(
        verbose_name="性质", max_length=1, null=True, blank=True,
        choices=MODE_CHOICES,
    )
    region = models.CharField(
        verbose_name="区域", max_length=1, null=True, blank=True,
        choices=REGION_CHOICES,
    )
    created_at = models.DateField(
        verbose_name="创建于", auto_now=True, editable=False,
    )
    altered_at = models.DateField(
        verbose_name="更改于", auto_now=True, null=True, blank=True,
    )
    materials = models.TextField(
        verbose_name="物料支持", null=True, blank=True
    )
    sponsorship = models.TextField(
        verbose_name="会议赞助支持", null=True, blank=True,
    )
    activities = models.TextField(
        verbose_name="策划活动支持", null=True, blank=True,
    )
    note = models.TextField(
        verbose_name="备注信息", max_length=128, null=True, blank=True,
    )

    class Meta:
        app_label = "partners"
        verbose_name = verbose_name_plural = "合作方"
    
    def __str__(self):
        return "%s" % self.name


class Propaganda(models.Model):
    partner = models.ForeignKey(
        Partners, verbose_name="合作方", on_delete=models.CASCADE
    )
    date = models.DateField(
        verbose_name="时间",
    )
    bms_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="宣讲人",
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "partners"
        verbose_name = verbose_name_plural = "宣讲"

    def __str__(self):
        return "【%s】的宣讲" % self.partner.name
