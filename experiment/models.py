from django.db import models
# Create your models here.
from tech_support.models import *


class ExtExecute(models.Model):
    """实验的提取表"""
    EXT_STATUS = (
        (0, '提取实验数据已上传，待审核'),
        (1, '实验已审核，进入质检环节'),
        (2, '特殊情况，自行控制'),
    )
    ext_number = models.CharField(
        "提取编号", max_length=50, blank=True, null=True
    )
    boxes = models.ForeignKey(
        Boxes, verbose_name="对应盒子信息",
        on_delete=models.SET_NULL, null=True
    )
    exp_method = models.ForeignKey(ExtMethod, verbose_name="实验方法",
                                   on_delete=models.SET_NULL, null=True)
    ext_method = models.CharField(
        verbose_name="提取方法", max_length=50, default=""
    )
    ext_times = models.IntegerField("提取次数", null=True)
    start_number = models.CharField("起始取样量(ml)", max_length=50, null=True)
    test_number = models.CharField("试管批次", max_length=50, null=True)
    hemoglobin = models.CharField("血红蛋白", max_length=50, null=True)
    cizhutiji = models.CharField("磁珠体积(ul)", max_length=50, null=True)
    ext_density = models.CharField("提取浓度(ng/ul)", max_length=50, null=True)
    elution_volume = models.CharField("洗脱体积(ul)", max_length=50, null=True)
    # produce = models.CharField("产出(ng)", max_length=50, null=True)
    operator = models.ForeignKey(AUTH_USER_MODEL, verbose_name="操作人员",
                                 on_delete=models.SET_NULL, null=True)
    ext_date = models.DateField("提取日期", null=True)
    note = models.TextField(verbose_name="实验异常备注", blank=True)
    status = models.IntegerField(
        choices=EXT_STATUS, verbose_name="状态", null=True
    )
    objective = models.CharField(
        verbose_name="目的", max_length=50, default=""
    )
    # submit = models.BooleanField(
    #     verbose_name='实验正常，进行下一步', null=True
    # )
    # fail = models.BooleanField(
    #     verbose_name='特殊情况，自行控制', null=True
    # )

    class Meta:
        app_label = "experiment"
        verbose_name = verbose_name_plural = "1-提取任务管理"

    def __str__(self):
        return self.ext_number


class QualityTest(models.Model):
    """实验的质检表"""
    QUA_STATUS = (
        (0, '质检实验数据已上传，待审核'),
        (1, '实验已审核，进入BS环节'),
        (2, '特殊情况，自行控制'),
    )
    qua_number = models.CharField("质检编号", max_length=50, null=True)
    boxes = models.ForeignKey(Boxes, verbose_name="对应盒子信息",
                              on_delete=models.SET_NULL, null=True)
    extexecute = models.ForeignKey(ExtExecute, verbose_name="提取信息",
                                   on_delete=models.SET_NULL, null=True)
    template_number = models.CharField("模板量", max_length=50, null=True)
    instrument = models.CharField("仪器", max_length=50, null=True)
    test_number = models.CharField("试管批次", max_length=50, null=True)
    loop_number = models.CharField("循环数", max_length=50, null=True)
    background_baseline = models.CharField("Background/Baseline",
                                           max_length=50, null=True)
    is_quality = models.BooleanField(verbose_name="有无质控", null=True)
    ct = models.CharField("非甲基化内参ACTB_CT值", max_length=50, null=True)
    amplification_curve = models.CharField("非甲基化内参ACTB_扩增曲线",
                                           max_length=50, null=True)
    noise = models.CharField(
        "非甲基化内参ACTB_Noise Band", max_length=50, null=True
    )
    operator = models.ForeignKey(AUTH_USER_MODEL, verbose_name="操作人员",
                                 on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(
        choices=QUA_STATUS, verbose_name="状态", null=True
    )
    qua_date = models.DateField("质检日期", null=True)
    note = models.TextField(verbose_name="实验异常备注", default="", blank=True)
    # submit = models.BooleanField(
    #     verbose_name='实验正常，进行下一步', null=True
    # )
    # fail = models.BooleanField(
    #     verbose_name='特殊情况，自行控制', null=True
    # )

    class Meta:
        app_label = "experiment"
        verbose_name = verbose_name_plural = "2-质检任务管理"

    def __str__(self):
        return self.qua_number


class BsTask(models.Model):
    """实验的BS表"""
    BS_STATUS = (
        (0, 'BS实验数据已上传，待审核'),
        (1, '实验已审核，进入荧光定量环节'),
        (2, '特殊情况，自行控制'),
    )
    bs_number = models.CharField("BS编号", max_length=50, null=True)
    boxes = models.ForeignKey(Boxes, verbose_name="对应盒子信息",
                              on_delete=models.SET_NULL, null=True)
    quality_Test = models.ForeignKey(QualityTest, verbose_name="质检信息",
                                     on_delete=models.SET_NULL, null=True)
    test_number = models.CharField(
        verbose_name="试管批次", max_length=50, null=True
    )
    bs_times = models.IntegerField(verbose_name="BS次数", null=True)
    bis_begin = models.CharField(
        verbose_name="BIS起始量(ng)", max_length=50, null=True
    )
    bis_template = models.CharField(
        verbose_name="BIS模板量(ul)", max_length=50
    )
    bis_elution = models.CharField(
        verbose_name="BIS洗脱体积(ul)", max_length=50
    )
    is_quality = models.BooleanField(verbose_name="有无质控", null=True)
    operator = models.ForeignKey(AUTH_USER_MODEL, verbose_name="操作人员",
                                 on_delete=models.SET_NULL, null=True)
    bs_date = models.DateField("BS实验日期", null=True)
    note = models.TextField(verbose_name="实验异常备注", blank=True, null=True)
    status = models.IntegerField(
        choices=BS_STATUS, verbose_name="状态", null=True)

    class Meta:
        app_label = "experiment"
        verbose_name = verbose_name_plural = "3-BS任务管理"

    def __str__(self):
        return self.bs_number


class FluorescenceQuantification(models.Model):
    """实验的荧光定量表"""
    FQ_STATUS = (
        (0, '荧光定量实验数据已上传，待审核'),
        (1, '实验已审核，进入结果判定环节'),
        (2, '特殊情况，自行控制'),
    )
    IS_QUALIFIED = (
        (0, '是'),
        (1, '否'),
        (2, '污染'),
    )
    boxes = models.ForeignKey(Boxes, verbose_name="对应盒子信息",
                              on_delete=models.SET_NULL, null=True)
    fq_number = models.CharField("荧光定量编号", max_length=50)
    bs_task = models.ForeignKey(BsTask, verbose_name="BS信息",
                                on_delete=models.SET_NULL, null=True)
    test_number = models.CharField(
        verbose_name="试管批次", max_length=50, null=True
    )
    instrument = models.CharField(
        verbose_name="仪器", max_length=50, null=True)
    loop_number = models.CharField(
        verbose_name="循环数", max_length=50, null=True
    )
    background = models.CharField(
        verbose_name="Background", max_length=50, null=True
    )
    actb_noise = models.CharField(
        verbose_name="ACTB_NoiseBand/STDMultiplier", max_length=50, null=True
    )
    actb_ct = models.CharField(verbose_name="ACTB_CT值", max_length=50,
                               null=True)
    actb_amp = models.CharField(
        verbose_name="ACTB_扩增曲线", max_length=50, null=True
    )
    sfrp2_noise = models.CharField(
        verbose_name="Sfrp2_NoiseBand/STDMultiplier",
        max_length=50, null=True)
    sfrp2_ct = models.CharField(verbose_name="Sfrp2_CT值", max_length=50,
                                null=True)
    sfrp2_amp = models.CharField(
        verbose_name="Sfrp2_扩增曲线", max_length=50, null=True
    )
    sdc2_noise = models.CharField(verbose_name="Sdc2_NoiseBand/STDMultiplier",
                                  max_length=50, null=True)
    sdc2_ct = models.CharField(verbose_name="Sdc2_CT值", max_length=50,
                               null=True)
    sdc2_amp = models.CharField(
        verbose_name="Sdc2_扩增曲线", max_length=50, null=True
    )
    is_quality = models.BooleanField(verbose_name="有无质控", null=True)
    operator = models.ForeignKey(AUTH_USER_MODEL, verbose_name="操作人员",
                                 on_delete=models.SET_NULL, null=True)
    fq_date = models.DateField("荧光定量日期", null=True)
    is_qualified = models.IntegerField(verbose_name="是否合格",
                                     choices=IS_QUALIFIED, null=True)
    qpcr_suggest = models.CharField("建议", max_length=200, null=True)
    status = models.IntegerField(
        choices=FQ_STATUS, verbose_name="状态", null=True
    )
    result = models.TextField(verbose_name="结果", null=True)
    note = models.TextField(verbose_name="实验异常备注", blank=True, null=True)


    class Meta:
        app_label = "experiment"
        verbose_name = verbose_name_plural = "4-荧光定量管理"

    def __str__(self):
        return self.fq_number


class ResultJudgement(models.Model):
    boxes = models.ForeignKey(Boxes, verbose_name="对应盒子信息",
                              on_delete=models.SET_NULL, null=True)
    fq = models.ForeignKey(
        FluorescenceQuantification, verbose_name="荧光定量信息",
        on_delete=models.SET_NULL, null=True)