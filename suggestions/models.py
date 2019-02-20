import re
from django.db import models
from products.models import Products


class Collections(models.Model):
    FACTOR_CHOICES = (
        (1, "经常"),
        (2, "偶尔"),
        (3, "从不"),
    )
    product = models.OneToOneField(
        Products, verbose_name="样品条码", on_delete=models.CASCADE
    )
    state_of_smoking = models.CharField(
        verbose_name="抽烟", max_length=2, choices=FACTOR_CHOICES
    )
    state_of_drinking = models.CharField(
        verbose_name="喝酒", max_length=2, choices=FACTOR_CHOICES
    )
    enteroscopy = models.BooleanField(
        verbose_name="肠镜", default=False,
    )
    polyp_or_cancer = models.BooleanField(
        verbose_name="直系肠癌史", default=False,
    )
    state_of_lower_digestive_tract = models.CharField(
        verbose_name="下消化道症状", max_length=512, null=True, blank=True,
    )
    state_of_specified_disease = models.CharField(
        verbose_name="以下其它病史", max_length=512, null=True, blank=True,
    )
    state_of_other_disease = models.CharField(
        verbose_name="其它慢性病史", max_length=512, null=True, blank=True,
    )
    notes = models.TextField(
        verbose_name="备注", null=True, blank=True,
    )
    kras_rate = models.DecimalField(
        verbose_name="KRAS突变率", null=True, blank=True,
    )
    bmp3_rate = models.DecimalField(
        verbose_name="BMP3突变率", null=True, blank=True,
    )
    ndrg4_rate = models.DecimalField(
        verbose_name="NDRG4突变率", null=True, blank=True,
    )
    hemoglobin = models.DecimalField(
        verbose_name="血红蛋白含量", null=True, blank=True,
    )
    final_score = models.SmallIntegerField(
        verbose_name="总得分", null=True, blank=True,
    )
    
    class Meta:
        verbose_name = verbose_name_plural = "健康建议与打分"

    def __str__(self):
        return '盒子{}'.format(self.product)


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
    
    def __str__(self):
        return self.name


class Choices(models.Model):
    code = models.CharField(
        verbose_name="选项代号", max_length=8, primary_key=True
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

    def __str__(self):
        return self.name


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
    
    @property
    def all_choices(self):
        factors = self.factors.all()
        choices = {factor.choices_set for factor in factors}
        return choices
    
    @property
    def expression_set(self):
        expressions_list = re.match("[【](.*?)[】]", self.expressions)
        return set(expressions_list.groups())
    
    def __str__(self):
        return self.code

