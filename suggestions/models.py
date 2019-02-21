from django.db import models
from products.models import Products


class MultiSelectFactors(models.Model):
    code = models.CharField(
        verbose_name="选项编号", max_length=6, primary_key=True
    )
    content = models.CharField(
        verbose_name="选项内容", max_length=256,
    )
    create_at = models.DateField(
        verbose_name="创建于", auto_now_add=True,
    )

    class Meta:
        abstract = True
        verbose_name = verbose_name_plural = "多选因子"

    def __str__(self):
        return self.content


class F05s(MultiSelectFactors):
    """下消化道症状"""
    
    class Meta:
        verbose_name = verbose_name_plural = "f05：下消化道症状"


class F06s(MultiSelectFactors):
    """其它病史"""
    
    class Meta:
        verbose_name = verbose_name_plural = "f06：其它病史"


class F07s(MultiSelectFactors):
    """慢性病史"""
    
    class Meta:
        verbose_name = verbose_name_plural = "f07：慢性病史"


class Collections(models.Model):
    F01_CHOICES = (
        ("f01c01", "经常"),
        ("f01c02", "偶尔"),
        ("f01c03", "从不"),
    )
    F02_CHOICES = (
        ("f02c01", "经常"),
        ("f02c02", "偶尔"),
        ("f02c03", "从不"),
    )
    F03_CHOICES = (
        ("f03c01", "有肠癌史"),
        ("f03c02", "有肠息肉史（已摘除）"),
        ("f03c03", "有肠息肉史（未摘除）"),
        ("f03c04", "以上均无"),
    )
    F04_CHOICES = (
        ("f04c01", "有"),
        ("f04c02", "没有"),
    )
    F08_CHOICES = (
        ("f08c01", "偏瘦"),
        ("f08c02", "正常"),
        ("f08c03", "偏胖"),
        ("f08c04", "肥胖"),
    )
    F09_CHOICES = (
        ("f09c01", "55岁以上"),
        ("f09c02", "55岁以下"),
    )
    F10_CHOICES = (
        ("f10c01", "低风险"),
        ("f10c02", "高风险"),
    )
    F11_CHOICES = (
        ("f11c01", "否"),
        ("f11c02", "是"),
    )
    F12_CHOICES = (
        ("f12c01", "阴性"),
        ("f12c02", "弱阳性"),
        ("f12c03", "阳性"),
    )
    product = models.OneToOneField(
        Products, verbose_name="样品条码", on_delete=models.CASCADE,
        primary_key=True
    )
    f01 = models.CharField(
        verbose_name="吸烟", max_length=6, null=True, blank=True,
        choices=F01_CHOICES, default="f01c01"
    )
    f02 = models.CharField(
        verbose_name="喝酒", max_length=6, null=True, blank=True,
        choices=F02_CHOICES, default="f02c01"
    )
    f03 = models.CharField(
        verbose_name="肠癌息肉史", max_length=6,
        null=True, blank=True, choices=F03_CHOICES, default="f03c04"
    )
    f04 = models.CharField(
        verbose_name="直系亲属肠癌息肉史", max_length=6, null=True, blank=True,
        choices=F04_CHOICES, default="f04c02"
    )
    _f05 = models.ManyToManyField(
        F05s, verbose_name="下消化道症状",
    )
    _f06 = models.ManyToManyField(
        F06s, verbose_name="指定病史",
    )
    _f07 = models.ManyToManyField(
        F07s, verbose_name="慢性病史",
    )
    f08 = models.CharField(
        verbose_name="身体指数", max_length=6, null=True, blank=True,
        choices=F08_CHOICES, default="f08c02",
    )
    f09 = models.CharField(
        verbose_name="年龄分段", max_length=6, null=True, blank=True,
        choices=F09_CHOICES, default="f09c01",
    )
    f10 = models.CharField(
        verbose_name="风险结果", max_length=6, null=True, blank=True,
        choices=F10_CHOICES, default="f10c01",
    )
    f11 = models.CharField(
        verbose_name="肠镜", max_length=6, null=True, blank=True,
        choices=F11_CHOICES, default="f11c01",
    )
    f12 = models.CharField(
        verbose_name="血红蛋白", max_length=6, null=True, blank=True,
        choices=F12_CHOICES, default="f12c01",
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
    suggestions = models.TextField(
        verbose_name="健康建议", null=True, blank=True, default=None
    )
    is_submit = models.BooleanField(
        verbose_name="是否提交", default=False
    )
    submitted_at = models.DateField(
        verbose_name="提交日期", auto_now=True
    )
    create_at = models.DateField(
        verbose_name="创建于", auto_now_add=True,
    )
    
    @property
    def f05(self):
        return {f05.code for f05 in self._f05.all()}
    
    @property
    def f06(self):
        return {f06.code for f06 in self._f06.all()}
    
    @property
    def f07(self):
        return {f07.code for f07 in self._f07.all()}
    
    class Meta:
        verbose_name = verbose_name_plural = "健康建议与打分"
    
    def __str__(self):
        return '样本{}'.format(self.product)


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
        return "{}-{}".format(self.code, self.name)


class Suggestions(models.Model):
    factors = models.ManyToManyField(
        Factors, verbose_name="关联因子",
    )
    code = models.CharField(
        verbose_name="建议代号", max_length=4, primary_key=True,
    )
    name = models.CharField(
        verbose_name="建议名称", max_length=64, null=True, blank=True,
    )
    connections = models.CharField(
        verbose_name="关联选项代号", max_length=128,
        help_text="参照可选择的选项输入，需要先选中关联因子保存，这里才可以显示"
    )
    expressions = models.TextField(
        verbose_name="表达形式",
    )
    
    # @property
    # def all_choices(self):
    #     factors = self.factors.all()
    #     choices = {factor.choices_set for factor in factors}
    #     return choices
    #
    # @property
    # def expression_set(self):
    #     expressions_list = re.match("[【](.*?)[】]", self.expressions)
    #     return set(expressions_list.groups())

    class Meta:
        verbose_name = verbose_name_plural = "建议语料库"

    def __str__(self):
        return self.code

