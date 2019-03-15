from django.db import models
from django.contrib.auth.models import AbstractUser


class BmsUser(AbstractUser):
    mobile_phone = models.CharField(
        verbose_name="手机号", max_length=11, null=True, blank=True
    )
    is_bound = models.BooleanField(
        verbose_name="绑定钉钉", default=False,
    )
    
    class Meta:
        verbose_name = verbose_name_plural = "用户"
    
    def __str__(self):
        return "【{}】".format(self.username)


class WechatInfo(models.Model):
    SEX_CHOICES = (
        ("0", u"未知"),
        ("1", u"男"),
        ("2", u"女"),
    )
    LIMIT_CHOICES_TO = {
        "is_staff": True,
        "is_superuser": False
    }
    bms_user = models.OneToOneField(
        BmsUser, verbose_name="用户", on_delete=models.CASCADE,
        limit_choices_to=LIMIT_CHOICES_TO, primary_key=True,
    )
    openid = models.CharField(
        verbose_name="唯一ID", max_length=64, null=True, blank=True,
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
        verbose_name = verbose_name_plural = "用户微信信息"

    def __str__(self):
        return "【{}】-【{}】".format(self.nickname, self.openid)


class DingtalkInfo(models.Model):
    SEX_CHOICES = (
        (0, "男"),
        (1, "女"),
    )
    LIMIT_CHOICES_TO = {
        "is_staff": True,
        "is_superuser": False,
    }
    bms_user = models.OneToOneField(
        BmsUser, verbose_name="用户", on_delete=models.CASCADE,
        limit_choices_to=LIMIT_CHOICES_TO, primary_key=True,
    )
    userid = models.CharField(
        verbose_name="唯一ID", max_length=64, null=True, blank=True,
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
        verbose_name="性别", null=True, blank=True, choices=SEX_CHOICES,
    )
    avatar = models.CharField(
        verbose_name="头像", max_length=512, null=True, blank=True,
    )
    unionid = models.CharField(
        verbose_name="应用内ID", max_length=64, null=True, blank=True,
    )
    
    class Meta:
        verbose_name = verbose_name_plural = "用户钉钉信息"

    def __str__(self):
        return "【{}】-【{}】".format(self.name, self.userid)


class DingtalkChat(models.Model):
    chat_id = models.CharField(
        verbose_name="群聊编号", primary_key=True, max_length=64,
    )
    name = models.CharField(
        verbose_name="群聊名称", max_length=32, null=True, blank=True,
        default="内部群聊",
    )
    owner = models.ForeignKey(
        DingtalkInfo, verbose_name="群主", related_name="chat_owner",
        on_delete=models.SET_NULL, null=True,
    )
    members = models.ManyToManyField(
        DingtalkInfo, verbose_name="群聊成员", related_name="chat_members",
    )
    create_at = models.DateField(
        verbose_name="创建时间", auto_now_add=True,
    )
    is_valid = models.BooleanField(
        verbose_name="是否有效", default=True,
    )
    
    class Meta:
        verbose_name_plural = verbose_name = "钉钉群组"
    
    def __str__(self):
        return '%s' % self.name


class ChatTemplates(models.Model):
    TEMPLATE_KIND = (
        "msg", u"文本消息"
        "2", u"msg"
        "3", u"msg"
    )
    name = models.CharField(
        verbose_name="名称", max_length=32, null=True, blank=True,
    )
    sign = models.CharField(
        verbose_name="签名", max_length=32, null=True, blank=True,
    )
    text = models.TextField(
        verbose_name="内容", null=True, blank=True,
    )
    link = models.CharField(
        verbose_name="链接", max_length=256, null=True, blank=True,
    )
    create_at = models.DateField(
        verbose_name="创建时间", auto_now_add=True
    )
    is_valid = models.BooleanField(
        verbose_name="是否有效", default=True
    )
    
    @property
    def msg_text(self):
        return self.sign + self.text
    
    class Meta:
        verbose_name_plural = verbose_name = "消息模板"
    
    def __str__(self):
        return '%s' % self.name
