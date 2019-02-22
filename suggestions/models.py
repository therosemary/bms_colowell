from django.db import models
from products.models import Products


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


def choices_select(code__contains=""):
    choices = Choices.objects.filter(code__contains=code__contains)
    return choices.values_list("code", "name")


class Collections(models.Model):
    product = models.OneToOneField(
        Products, verbose_name="样品条码", on_delete=models.CASCADE,
        primary_key=True
    )
    f01 = models.CharField(
        verbose_name="吸烟", max_length=6, null=True, blank=True,
        choices=choices_select(code__contains="f01"), default="f01c01"
    )
    f02 = models.CharField(
        verbose_name="喝酒", max_length=6, null=True, blank=True,
        choices=choices_select(code__contains="f02"), default="f02c01"
    )
    f03 = models.CharField(
        verbose_name="肠癌息肉史", max_length=6, null=True, blank=True,
        choices=choices_select(code__contains="f03"), default="f03c04"
    )
    f04 = models.CharField(
        verbose_name="直系亲属肠癌息肉史", max_length=6, null=True, blank=True,
        choices=choices_select(code__contains="f04"),
        default="f04c02"
    )
    _f05 = models.ManyToManyField(
        Choices, verbose_name="下消化道症状", blank=True,
        limit_choices_to={"code__contains": "f05"},
        related_name="collections_f05",
    )
    _f06 = models.ManyToManyField(
        Choices, verbose_name="指定病史",  blank=True,
        limit_choices_to={"code__contains": "f06"},
        related_name = "collections_f06",
    )
    _f07 = models.ManyToManyField(
        Choices, verbose_name="慢性病史",  blank=True,
        limit_choices_to={"code__contains": "f07"},
        related_name = "collections_f07",
    )
    f08 = models.CharField(
        verbose_name="身体指数", max_length=6, null=True, blank=True,
        choices=choices_select(code__contains="f08"), default="f08c02",
    )
    f09 = models.CharField(
        verbose_name="年龄分段", max_length=6, null=True, blank=True,
        choices=choices_select(code__contains="f09"), default="f09c01",
    )
    f10 = models.CharField(
        verbose_name="风险结果", max_length=6, null=True, blank=True,
        choices=choices_select(code__contains="f10"), default="f10c01",
    )
    f11 = models.CharField(
        verbose_name="肠镜", max_length=6, null=True, blank=True,
        choices=choices_select(code__contains="f11"), default="f11c01",
    )
    f12 = models.CharField(
        verbose_name="血红蛋白", max_length=6, null=True, blank=True,
        choices=choices_select(code__contains="f12"), default="f12c01",
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


class Suggestions(models.Model):
    factors = models.ManyToManyField(
        Factors, verbose_name="关联因子", blank=True,
    )
    code = models.CharField(
        verbose_name="建议代号", max_length=4, primary_key=True,
    )
    name = models.CharField(
        verbose_name="建议名称", max_length=64, null=True, blank=True,
    )
    connections = models.CharField(
        verbose_name="关联选项代号", max_length=128, null=True, blank=True,
        help_text="参照可选择的选项输入，需要先选中关联因子保存，这里才可以显示"
    )
    expressions = models.TextField(
        verbose_name="表达形式", null=True, blank=True,
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
