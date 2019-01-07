from django.db import models
from tech_support.models import *


class ExtExecute(models.Model):
    """实验的提取表"""
    EXT_STATUS = (
        (0, '实验进行中'),
        (1, '实验成功，数据已提交'),
        (2, '实验重做，不提交数据'),
    )
    ext_number = models.CharField(
        verbose_name="提取编号", max_length=50
    )
    boxes = models.ForeignKey(
        BoxDeliveries, verbose_name="对应盒子信息", on_delete=models.SET_NULL,
        null=True,
    )
    ext_method = models.ForeignKey(
        ExtMethod, verbose_name="实验方法", on_delete=models.SET_NULL,
        null=True,
    )
    ext_times = models.IntegerField(
        verbose_name="提取次数"
    )
    start_number = models.CharField(
        verbose_name="起始取样量(ml)", max_length=50
    )
    test_number = models.CharField(
        verbose_name="试管批次", max_length=50
    )
    hemoglobin = models.CharField(
        verbose_name="血红蛋白", max_length=50
    )
    cizhutiji = models.CharField(
        verbose_name="磁珠体积(ul)", max_length=50
    )
    ext_density = models.CharField(
        verbose_name="提取浓度(ng/ul)"
    )
    elution_volume = models.CharField(
        verbose_name="洗脱体积(ul)", max_length=50
    )
    produce = models.CharField(
        verbose_name="产出(ng)", max_length=50
    )
    operator = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="操作人员", on_delete=models.SET_NULL,
        null=True,
    )
    ext_date = models.DateField(
        verbose_name="提取日期", null=True
    )
    note = models.TextField(
        verbose_name="实验异常备注",
    )
    status = models.IntegerField(
        verbose_name="状态", choices=EXT_STATUS,
    )


class QualityTest(models.Model):
    """实验的质检表"""
    QUA_STATUS = (
        (0, '实验进行中'),
        (1, '实验成功，数据已提交'),
        (2, '实验重做，不提交数据'),
    )
    qua_number = models.CharField(
        verbose_name="质检编号", max_length=50
    )
    boxes = models.ForeignKey(
        BoxDeliveries, verbose_name="对应盒子信息", on_delete=models.SET_NULL,
        null=True,
    )
    extexecute = models.ForeignKey(
        ExtExecute, verbose_name="提取信息", on_delete=models.SET_NULL,
        null=True,
    )
    template_number = models.CharField(
        verbose_name="模板量", max_length=50,
    )
    instrument = models.CharField(
        verbose_name="仪器", max_length=50,
    )
    test_number = models.CharField(
        verbose_name="试管批次", max_length=50,
    )
    loop_number = models.CharField(
        verbose_name="循环数", max_length=50,
    )
    background_baseline = models.CharField(
        verbose_name="Background/Baseline", max_length=50,
    )
    ct = models.CharField(
        verbose_name="非甲基化ACTB-CT值", max_length=50,
    )
    amplification_curve = models.CharField(
        verbose_name="非甲基化ACTB-扩增曲线", max_length=50,
    )
    threshold_line = models.CharField(
        verbose_name="非甲基化ACTB-阀值线", max_length=50,
    )
    operator = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="操作人员", on_delete=models.SET_NULL,
        null=True,
    )
    status = models.IntegerField(
        verbose_name="状态", choices=QUA_STATUS,
    )
    qua_date = models.DateField(
        verbose_name="质检日期", null=True
    )


class BsTask(models.Model):
    """实验的BS表"""
    BS_STATUS = (
        (0, '实验进行中'),
        (1, '实验成功，数据已提交'),
        (2, '实验重做，不提交数据'),
    )
    bs_number = models.CharField(
        verbose_name="BS编号", max_length=50,
    )
    boxes = models.ForeignKey(
        BoxDeliveries, verbose_name="对应盒子信息", on_delete=models.SET_NULL,
        null=True,
    )
    quality_Test = models.ForeignKey(
        QualityTest, verbose_name="质检信息", on_delete=models.SET_NULL,
        null=True,
    )
    test_number = models.CharField(
        verbose_name="试管批次", max_length=50,
    )
    bs_times = models.IntegerField(
        verbose_name="BS次数",
    )
    bis_begin = models.CharField(
        verbose_name="BIS起始量(ng)", max_length=50,
    )
    bis_template = models.CharField(
        verbose_name="BIS模板量(ul)", max_length=50,
    )
    bis_elution = models.CharField(
        verbose_name="bis洗脱体积(ul)", max_length=50,
    )
    is_quality = models.BooleanField(
        verbose_name="有无质控",
    )
    operator = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="操作人员", on_delete=models.SET_NULL,
        null=True,
    )
    bs_date = models.DateField(
        verbose_name="BS实验日期", null=True,
    )
    note = models.TextField(
        verbose_name="实验异常备注",
    )
    status = models.IntegerField(
        verbose_name="状态", choices=BS_STATUS,
    )


class FluorescenceQuantification(models.Model):
    """实验的荧光定量表"""
    FQ_STATUS = (
        (0, '实验进行中'),
        (1, '实验成功，数据已提交'),
        (2, '实验重做，不提交数据'),
        (3, '实验数据已核对'),
    )
    boxes = models.ForeignKey(
        BoxDeliveries, verbose_name="对应盒子信息", on_delete=models.SET_NULL,
        null=True,
    )
    fq_number = models.CharField(
        verbose_name="荧光定量编号", max_length=50,
    )
    bs_task = models.ForeignKey(
        BsTask, verbose_name="BS信息", on_delete=models.SET_NULL, null=True,
    )
    test_number = models.CharField(
        verbose_name="试管批次", max_length=50,
    )
    instrument = models.CharField(
        verbose_name="仪器", max_length=50,
    )
    loop_number = models.CharField(
        verbose_name="循环数", max_length=50,
    )
    background = models.CharField(
        verbose_name="Background", max_length=50,
    )
    actb_noise = models.CharField(
        verbose_name="内参ACTB--NoiseBand/STDMultiplier", max_length=50,
    )
    actb_ct = models.CharField(
        verbose_name="内参ACTB--CT值", max_length=50,
    )
    actb_amp = models.CharField(
        verbose_name="内参ACTB--扩增曲线", max_length=50,
    )
    sfrp2_noise = models.CharField(
        verbose_name="sfrp2--NoiseBand/STDMultiplier", max_length=50,
    )
    sfrp2_ct = models.CharField(
        verbose_name="sfrp2--CT值", max_length=50,
    )
    sfrp2_amp = models.CharField(
        verbose_name="sfrp2--扩增曲线", max_length=50,
    )
    sdc2_noise = models.CharField(
        verbose_name="sdc2--NoiseBand/STDMultiplier", max_length=50,
    )
    sdc2_ct = models.CharField(
        verbose_name="sdc2--CT值", max_length=50,
    )
    sdc2_amp = models.CharField(
        verbose_name="sdc2--扩增曲线", max_length=50,
    )
    is_quality = models.BooleanField(
        verbose_name="有无质控",
    )
    operator = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="操作人员", on_delete=models.SET_NULL,
        null=True,
    )
    fq_date = models.DateField(
        verbose_name="荧光定量日期", null=True,
    )
    qpcr_index = models.CharField(
        verbose_name="QPCR反馈", max_length=50,
    )
    qpcr_suggest = models.CharField(
        verbose_name="建议", max_length=200,
    )
    status = models.IntegerField(
        verbose_name="状态", choices=FQ_STATUS,
    )
    result = models.TextField(
        verbose_name="结果"
    )
