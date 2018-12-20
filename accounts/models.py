from django.db import models
from django.contrib.auth.models import AbstractUser


class BmsUser(AbstractUser):
    mobile_phone = models.CharField(
        verbose_name="手机号", max_length=11, null=True, blank=True
    )

    class Meta:
        app_label = "accounts"
        verbose_name = verbose_name_plural = "用户"
    
    def __str__(self):
        return "【{}】".format(self.username)


class WechatInfo(models.Model):
    SEX_CHOICES = (
        ("0", u"未知"),
        ("1", u"男"),
        ("2", u"女"),
    )
    bms_user = models.OneToOneField(
        BmsUser, verbose_name="用户", on_delete=models.CASCADE
    )
    openid = models.CharField(
        verbose_name="微信唯一ID", max_length=64, primary_key=True,
    )
    nickname = models.CharField(
        verbose_name="昵称", max_length=32, null=True, blank=True,
    )
    sex = models.PositiveSmallIntegerField(
        verbose_name="性别", null=True, blank=True, choices=SEX_CHOICES
    )
    city = models.CharField(
        verbose_name="城市", max_length=32, null=True, blank=True,
    )
    province = models.CharField(
        verbose_name="省份", max_length=32, null=True, blank=True,
    )
    country = models.CharField(
        verbose_name="国家", max_length=16, null=True, blank=True,
    )
    headimgurl = models.CharField(
        verbose_name="头像", max_length=512, null=True, blank=True,
    )
    unionid = models.CharField(
        verbose_name="公众号内ID", max_length=64, null=True, blank=True,
    )
    
    class Meta:
        app_label = "accounts"
        verbose_name = verbose_name_plural = "用户微信信息"

    def __str__(self):
        return "【{}】-【{}】".format(self.nickname, self.openid)


class DingtalkInfo(models.Model):
    bms_user = models.OneToOneField(
        BmsUser, verbose_name="用户", on_delete=models.CASCADE
    )
    userid = models.CharField(
        verbose_name="钉钉唯一ID", max_length=64, primary_key=True,
    )
    name = models.CharField(
        verbose_name="昵称", max_length=32, null=True, blank=True,
    )
    position = models.CharField(
        verbose_name="职位", max_length=32, null=True, blank=True,
    )
    jobnumber = models.CharField(
        verbose_name="工号", max_length=32, null=True, blank=True,
    )
    sex = models.PositiveSmallIntegerField(
        verbose_name="性别", null=True, blank=True
    )
    avatar = models.CharField(
        verbose_name="头像", max_length=512, null=True, blank=True,
    )
    unionid = models.CharField(
        verbose_name="应用内ID", max_length=64, null=True, blank=True,
    )
    
    class Meta:
        app_label = "accounts"
        verbose_name = verbose_name_plural = "用户钉钉信息"

    def __str__(self):
        return "【{}】-【{}】".format(self.name, self.userid)


class Partners(models.Model):
    partner = models.OneToOneField(
        BmsUser, verbose_name="合作方", on_delete=models.CASCADE
    )
    store_code = models.CharField(
        verbose_name="编号", max_length=32, primary_key=True,
    )
    store_name = models.CharField(
        verbose_name="名称", max_length=32, null=True, blank=True,
    )
    created_at = models.DateField(
        verbose_name="创建于", auto_now=True, editable=False,
    )
    altered_at = models.DateField(
        verbose_name="更改于", auto_now=True, null=True, blank=True,
    )
    store_note = models.TextField(
        verbose_name="备注", null=True, blank=True,
    )
    
    class Meta:
        app_label = "accounts"
        verbose_name = verbose_name_plural = "合作方"
    
    def __str__(self):
        return "%s" % self.store_name
