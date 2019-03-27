from django.db import models
from bms_colowell.settings import AUTH_USER_MODEL
from suggestions.models import Collections
from tech_support.models import Techsupport


class Experiments(models.Model):
    """实验管理"""
    index_number = models.CharField(
        verbose_name="实验编号", max_length=50, blank=True, null=False,
        primary_key=True
    )
    boxes = models.ForeignKey(
        Techsupport, verbose_name="对应盒子信息",
        on_delete=models.SET_NULL, null=True
    )
    receive_date = models.DateField(verbose_name="收样日期", null=True)
    projects_source = models.CharField(
        verbose_name="检测项目来源", max_length=50, blank=True, null=True
    )
    # 提取环节
    ext_method = models.CharField(
        verbose_name="提取-提取方法", max_length=50, blank=True, null=True
    )
    ext_objective = models.CharField(
        verbose_name="提取-目的", max_length=50, blank=True, null=True
    )
    ext_start_number = models.CharField(
        verbose_name="提取-起始取样量(ml)", max_length=50, blank=True, null=True
    )
    ext_hemoglobin = models.CharField(
        verbose_name="提取-血红蛋白", max_length=50,
        # choices=(
        #     ('阴性', u'初级'),
        #     ('zj', u'中级'),
        #     ('gj', u'高级'),
        #     ('gj', u'高级')),
        blank=True, null=True)
    ext_cz_volume = models.CharField(
        verbose_name="提取-磁珠体积(ul)", max_length=50, blank=True, null=True)
    ext_density = models.CharField(
        verbose_name="提取-提取浓度(ng/ul)", max_length=50, blank=True,
        null=True)
    ext_elution_volume = models.CharField("提取-洗脱体积(ul)", max_length=50,
                                          blank=True, null=True)
    ext_operator = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="提取-操作人员", on_delete=models.SET_NULL,
        blank=True, null=True, related_name="提取-操作人员+")
    ext_date = models.DateField(verbose_name="提取-日期", blank=True, null=True)
    ext_note = models.TextField(
        verbose_name="提取-实验备注", blank=True, null=True)
    submit_ext = models.BooleanField(verbose_name="提取-提交", default=False)
    # 质检环节
    qua_test_number = models.CharField(
        verbose_name="质检-试剂批次", max_length=50, blank=True, null=True)
    qua_sample_size = models.CharField(
        verbose_name="质检-上样量", max_length=50, blank=True, null=True)
    qua_instrument = models.CharField(
        verbose_name="质检-仪器", max_length=50, blank=True, null=True)
    qua_loop_number = models.CharField(
        verbose_name="质检-循环数", max_length=50, blank=True, null=True)
    qua_background = models.CharField(
        verbose_name="质检-Background", max_length=50, blank=True, null=True)
    qua_noise = models.CharField(
        verbose_name="质检-非甲基化内参ACTB_Noise Band", max_length=50,
        blank=True, null=True)
    qua_ct = models.CharField(
        verbose_name="质检-非甲基化内参ACTB_CT值", max_length=50, blank=True,
        null=True)
    qua_amplification_curve = models.CharField(
        verbose_name="质检-非甲基化内参ACTB_扩增曲线", max_length=50, blank=True,
        null=True)
    qua_is_quality = models.BooleanField(
        verbose_name="质检-有无质控", blank=True, null=True)
    qua_operator = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="质检-操作人员", on_delete=models.SET_NULL,
        blank=True, null=True, related_name="质检-操作人员+")
    qua_date = models.DateField(verbose_name="质检-日期", blank=True, null=True)
    qua_note = models.TextField(
        verbose_name="质检-实验备注", blank=True, null=True)
    submit_qua = models.BooleanField(verbose_name="质检-提交", default=False)
    # BS环节
    bis_test_number = models.CharField(
        verbose_name="BIS-试剂批次", max_length=50, blank=True, null=True
    )
    bis_begin = models.CharField(
        verbose_name="BIS-起始量(ng)", max_length=50, blank=True, null=True
    )
    bis_template = models.CharField(
        verbose_name="BIS-模板量(ul)", max_length=50, blank=True, null=True
    )
    bis_elution = models.CharField(
        verbose_name="BIS-洗脱体积(ul)", max_length=50, blank=True, null=True
    )
    bis_is_quality = models.BooleanField(
        verbose_name="BIS-有无质控", blank=True, null=True)
    bis_operator = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="BIS-操作人员", on_delete=models.SET_NULL,
        blank=True, null=True, related_name="BIS-操作人员+")
    bis_date = models.DateField(verbose_name="BIS-日期", blank=True, null=True)
    bis_note = models.TextField(
        verbose_name="BIS-实验备注", blank=True, null=True)
    submit_bis = models.BooleanField(verbose_name="BIS-提交", default=False)
    # 荧光定量
    fq_test_number = models.CharField(
        verbose_name="荧光定量-试剂批次", max_length=50, blank=True, null=True
    )
    fq_instrument = models.CharField(
        verbose_name="荧光定量-仪器", max_length=50, blank=True, null=True)
    fq_loop_number = models.CharField(
        verbose_name="荧光定量-循环数", max_length=50, blank=True, null=True)
    # fq_background = models.CharField(
    #     verbose_name="荧光定量-Background", max_length=50, blank=True, null=True
    # )
    # fq_actb_noise = models.CharField(
    #     verbose_name="荧光定量-ACTB_NoiseBand/STDMultiplier", max_length=50,
    #     blank=True, null=True
    # )
    fq_actb_ct = models.CharField(verbose_name="荧光定量-ACTB_CT值",
                                  max_length=50, blank=True, null=True)
    fq_actb_amp = models.CharField(
        verbose_name="荧光定量-ACTB_扩增曲线", max_length=50, blank=True,
        null=True
    )
    # fq_sfrp2_noise = models.CharField(
    #     verbose_name="荧光定量-Sfrp2_NoiseBand/STDMultiplier",
    #     max_length=50, blank=True, null=True)
    fq_sfrp2_ct = models.CharField(verbose_name="荧光定量-Sfrp2_CT值",
                                   max_length=50, blank=True, null=True)
    fq_sfrp2_amp = models.CharField(
        verbose_name="荧光定量-Sfrp2_扩增曲线", max_length=50, blank=True,
        null=True
    )
    # fq_sdc2_noise = models.CharField(
    #     verbose_name="荧光定量-Sdc2_NoiseBand/STDMultiplier", max_length=50,
    #     blank=True, null=True)
    fq_sdc2_ct = models.CharField(
        verbose_name="荧光定量-Sdc2_CT值", max_length=50, blank=True, null=True)
    fq_sdc2_amp = models.CharField(
        verbose_name="荧光定量-Sdc2_扩增曲线", max_length=50, blank=True,
        null=True)
    fq_is_quality = models.BooleanField(
        verbose_name="荧光定量-有无质控", blank=True, null=True)
    fq_operator = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="荧光定量-操作人员",
        on_delete=models.SET_NULL, blank=True,
        null=True, related_name="荧光定量-操作人员+")
    fq_date = models.DateField(
        verbose_name="荧光定量-日期", blank=True, null=True)
    fq_suggest = models.CharField(
        verbose_name="荧光定量-建议", max_length=300, blank=True, null=True)
    submit_fq = models.BooleanField(verbose_name="荧光定量-提交", default=False)

    class Meta:
        app_label = "experiments"
        verbose_name = verbose_name_plural = "实验管理"

    def __str__(self):
        return self.index_number


class ResultJudgement(models.Model):
    experiment = models.OneToOneField(
        to=Experiments, verbose_name="对应实验", blank=True, null=True,
        on_delete=models.SET_NULL)
    collection = models.OneToOneField(
        to=Collections, verbose_name="对应调查问卷", blank=True, null=True,
        on_delete=models.SET_NULL)
    risk = models.CharField(verbose_name="风险性", choices=(("high", u"高风险"),
                                                            ("low", u"低风险")),
                            blank=True, null=True, max_length=20)
    SDC2 = models.CharField(verbose_name="SDC2基因检测结果", max_length=20,
                            choices=(("yin", u"阴性"),
                                     ("yang", u"阳性")),
                            blank=True, null=True)
    SFRP2 = models.CharField(verbose_name="SFRP2基因检测结果", max_length=20,
                             choices=(("yin", u"阴性"),
                                     ("yang", u"阳性")),
                             blank=True, null=True)
    res_date = models.DateField(verbose_name="判定日期", blank=True, null=True)
    risk_file = models.FileField(verbose_name="风险评估报告",
                                 upload_to="riskfile", blank=True, null=True)
    submit = models.BooleanField(verbose_name="提交", blank=True, default=False)

    class Meta:
        app_label = "experiments"
        verbose_name = verbose_name_plural = "结果判定"

    def __str__(self):
        return self.experiment.index_number
