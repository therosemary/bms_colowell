import os
import re
from django.db import models
from products.models import Products


def upload_to(obj, filename):
    code = obj.code if obj else "V00"
    return os.path.join("suggestions", code, filename)


class Factors(models.Model):
    code = models.CharField(
        verbose_name="因子代号", max_length=4, primary_key=True,
    )
    name = models.CharField(
        verbose_name="因子名称", max_length=32,
    )
    create_at = models.DateField(
        verbose_name="创建于", auto_now_add=True,
    )
    
    class Meta:
        verbose_name = verbose_name_plural = "建议因子"
    
    def __str__(self):
        return "{}-{}".format(self.code, self.name)


class Choices(models.Model):
    code = models.CharField(
        verbose_name="选项代号", max_length=8, default="f0c0",
        primary_key=True,
    )
    name = models.CharField(
        verbose_name="选项名称", max_length=64,
    )
    create_at = models.DateField(
        verbose_name="创建于", auto_now_add=True,
    )
    factor = models.ForeignKey(
        Factors, verbose_name="因子", on_delete=models.CASCADE
    )
    
    class Meta:
        verbose_name = verbose_name_plural = "建议因子选项"
    
    def __str__(self):
        return "{}".format(self.name)


class Versions(models.Model):
    code = models.CharField(
        verbose_name="版本代号", max_length=3, default="V01",
        help_text="版本号由V+数字组成，V代表Version，后面数字代表具体版本",
        primary_key=True,
    )
    name = models.CharField(
        verbose_name="版本名称", max_length=64,
    )
    t01_length_min = models.SmallIntegerField(
        verbose_name="饮食建议字数最少", default=0,
    )
    t02_length_min = models.SmallIntegerField(
        verbose_name="生活方式字数最少", default=0,
    )
    t03_length_min = models.SmallIntegerField(
        verbose_name="体育锻炼字数最少", default=0,
    )
    t04_length_min = models.SmallIntegerField(
        verbose_name="健康乐观心态字数最少", default=0,
    )
    t05_length_min = models.SmallIntegerField(
        verbose_name="定期筛查字数最少", default=0,
    )
    t06_length_min = models.SmallIntegerField(
        verbose_name="确诊和治疗字数最少", default=0,
    )
    t07_length_min = models.SmallIntegerField(
        verbose_name="肠镜检查准备字数最少", default=0,
    )
    t01_length_max = models.SmallIntegerField(
        verbose_name="饮食建议字数最多", default=100,
    )
    t02_length_max = models.SmallIntegerField(
        verbose_name="生活方式字数最多", default=100,
    )
    t03_length_max = models.SmallIntegerField(
        verbose_name="体育锻炼字数最多", default=100,
    )
    t04_length_max = models.SmallIntegerField(
        verbose_name="健康乐观心态字数最多", default=100,
    )
    t05_length_max = models.SmallIntegerField(
        verbose_name="定期筛查字数最多", default=100,
    )
    t06_length_max = models.SmallIntegerField(
        verbose_name="确诊和治疗字数最多", default=100,
    )
    t07_length_max = models.SmallIntegerField(
        verbose_name="肠镜检查准备字数最多", default=100,
    )
    reviewer = models.ImageField(
        verbose_name="复核人", upload_to=upload_to,
        default="suggestions/reviewer.png",
    )
    auditor = models.ImageField(
        verbose_name="批准人", upload_to=upload_to,
        default="suggestions/auditor.png",
    )
    tester = models.ImageField(
        verbose_name="检测人", upload_to=upload_to,
        default="suggestions/tester.png",
    )
    disclaimer = models.ImageField(
        verbose_name="声明方", upload_to=upload_to,
        default="suggestions/disclaimer.png",
    )
    signature = models.ImageField(
        verbose_name="盖章", upload_to=upload_to,
        default="suggestions/signature.png",
    )
    create_at = models.DateField(
        verbose_name="创建于", auto_now_add=True,
    )

    class Meta:
        verbose_name = verbose_name_plural = "报告版本"
    
    def __str__(self):
        return "{}".format(self.name)


class Collections(models.Model):
    product = models.OneToOneField(
        Products, verbose_name="样品条码", on_delete=models.CASCADE,
        primary_key=True
    )
    version = models.ForeignKey(
        Versions, verbose_name="报告版本", on_delete=models.CASCADE,
        default="V01",
    )
    _f01 = models.ForeignKey(
        Choices, verbose_name="吸烟", on_delete=models.SET_NULL,
        limit_choices_to={"code__contains": "f01"}, null=True,
        default="f01c01", related_name="collections_f01",
    )
    _f02 = models.ForeignKey(
        Choices, verbose_name="喝酒", on_delete=models.SET_NULL,
        limit_choices_to={"code__contains": "f02"}, null=True,
        default="f02c01", related_name="collections_f02",
    )
    _f03 = models.ForeignKey(
        Choices, verbose_name="本人肠癌息肉史", on_delete=models.SET_NULL,
        limit_choices_to={"code__contains": "f03"}, null=True,
        default="f03c04", related_name="collections_f03",
    )
    _f04 = models.ForeignKey(
        Choices, verbose_name="直系亲属肠癌息肉史", on_delete=models.SET_NULL,
        limit_choices_to={"code__contains": "f04"}, null=True,
        default="f04c02", related_name="collections_f04",
    )
    _f05 = models.ManyToManyField(
        Choices, verbose_name="下消化道症状", blank=True,
        limit_choices_to={"code__contains": "f05"},
        related_name="collections_f05",
    )
    _f06 = models.ManyToManyField(
        Choices, verbose_name="指定病史",  blank=True,
        limit_choices_to={"code__contains": "f06"},
        related_name="collections_f06",
    )
    _f07 = models.ManyToManyField(
        Choices, verbose_name="慢性病史",  blank=True,
        limit_choices_to={"code__contains": "f07"},
        related_name="collections_f07",
    )
    _f08 = models.ForeignKey(
        Choices, verbose_name="身体指数", on_delete=models.SET_NULL,
        limit_choices_to={"code__contains": "f08"}, null=True,
        default="f08c02", related_name="collections_f08",
    )
    _f09 = models.ForeignKey(
        Choices, verbose_name="年龄分段", on_delete=models.SET_NULL,
        limit_choices_to={"code__contains": "f09"}, null=True,
        default="f09c01", related_name="collections_f09",
    )
    _f10 = models.ForeignKey(
        Choices, verbose_name="风险结果", on_delete=models.SET_NULL,
        limit_choices_to={"code__contains": "f10"}, null=True,
        default="f10c01", related_name="collections_f10",
    )
    _f11 = models.ForeignKey(
        Choices, verbose_name="肠镜", on_delete=models.SET_NULL,
        limit_choices_to={"code__contains": "f11"}, null=True,
        default="f11c01", related_name="collections_f11",
    )
    _f12 = models.ForeignKey(
        Choices, verbose_name="血红蛋白", on_delete=models.SET_NULL,
        limit_choices_to={"code__contains": "f12"}, null=True,
        default="f12c01", related_name="collections_f12",
    )
    kras_mutation_rate = models.DecimalField(
        verbose_name="KRAS突变率", max_digits=5, decimal_places=4,
        null=True, blank=True,
    )
    bmp3_mutation_rate = models.DecimalField(
        verbose_name="BMP3突变率", max_digits=5, decimal_places=4,
        null=True, blank=True,
    )
    ndrg4_mutation_rate = models.DecimalField(
        verbose_name="NDRG4突变率", max_digits=5, decimal_places=4,
        null=True, blank=True,
    )
    hemoglobin_content = models.DecimalField(
        verbose_name="血红蛋白含量", max_digits=5, decimal_places=2,
        null=True, blank=True,
    )
    score = models.SmallIntegerField(
        verbose_name="总得分", null=True, blank=True,
    )
    t01 = models.TextField(
        verbose_name="饮食建议", null=True, blank=True, default=None
    )
    t02 = models.TextField(
        verbose_name="生活方式", null=True, blank=True, default=None
    )
    t03 = models.TextField(
        verbose_name="体育锻炼", null=True, blank=True, default=None
    )
    t04 = models.TextField(
        verbose_name="健康乐观心态", null=True, blank=True, default=None
    )
    t05 = models.TextField(
        verbose_name="定期筛查", null=True, blank=True, default=None
    )
    t06 = models.TextField(
        verbose_name="确诊和治疗", null=True, blank=True, default=None
    )
    t07 = models.TextField(
        verbose_name="肠镜检查准备", null=True, blank=True, default=None
    )
    suggestions = models.TextField(
        verbose_name="健康建议", null=True, blank=True, default=None
    )
    is_submit = models.BooleanField(
        verbose_name="是否提交", default=False
    )
    pdf_upload = models.FileField(
        verbose_name="报告上传", null=True, blank=True, upload_to="report/",
    )
    download_url = models.URLField(
        verbose_name="报告下载", null=True, blank=True,
    )
    submitted_at = models.DateField(
        verbose_name="提交日期", auto_now=True
    )
    create_at = models.DateField(
        verbose_name="创建于", auto_now_add=True,
    )
    
    @property
    def f01(self):
        return self._f01.code
    
    @property
    def f02(self):
        return self._f02.code
    
    @property
    def f03(self):
        return self._f03.code
    
    @property
    def f04(self):
        return self._f04.code
    
    @property
    def f05(self):
        return ";".join([f05.code for f05 in self._f05.all()])
    
    @property
    def f06(self):
        return ";".join([f06.code for f06 in self._f06.all()])
    
    @property
    def f07(self):
        return ";".join([f07.code for f07 in self._f07.all()])

    @property
    def f08(self):
        return self._f08.code

    @property
    def f09(self):
        return self._f09.code

    @property
    def f10(self):
        return self._f10.code

    @property
    def f11(self):
        return self._f11.code

    @property
    def f12(self):
        return self._f12.code

    class Meta:
        verbose_name = verbose_name_plural = "健康建议与打分"
    
    def __str__(self):
        return '样本{}'.format(self.product)


class Types(models.Model):
    code = models.CharField(
        verbose_name="类别代号", max_length=3, primary_key=True,
        default="t0x",
    )
    name = models.CharField(
        verbose_name="类别名称", max_length=64, null=True, blank=True,
    )
    create_at = models.DateField(
        verbose_name="创建于", auto_now_add=True,
    )

    class Meta:
        verbose_name = verbose_name_plural = "建议类别"

    def __str__(self):
        return "{}".format(self.name)


class Suggestions(models.Model):
    factors = models.ManyToManyField(
        Factors, verbose_name="关联因子", blank=True,
    )
    code = models.CharField(
        verbose_name="建议代号", max_length=6, primary_key=True,
        help_text="【建议代号】共6位，前三位代表类别txx，后三位代表该类别下的序号sxx",
        default="t00s00",
    )
    type_name = models.ForeignKey(
        Types, verbose_name="类别名称", on_delete=models.SET_NULL, null=True,
    )
    connections = models.CharField(
        verbose_name="关联选项代号", max_length=512, null=True, blank=True,
        help_text="这里选择要选择的选项，选项之间用英文的分号分隔开"
    )
    expressions = models.TextField(
        verbose_name="表达形式", null=True, blank=True,
    )
    is_required = models.BooleanField(
        verbose_name="是否必要", default=False,
    )
    
    @property
    def _factors(self):
        return [factor.code for factor in self.factors.all().order_by("code")]
    
    @property
    def _choices(self):
        return self.connections.split(";") if self.connections else ""

    @property
    def sentences(self):
        return re.findall(r"[【]([\s\S]*?)[】]", self.expressions)
    
    class Meta:
        verbose_name = verbose_name_plural = "建议语料"
    
    def __str__(self):
        return self.code
