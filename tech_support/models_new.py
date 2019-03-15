from django.db import models
from bms_colowell.settings import AUTH_USER_MODEL
from partners.models import Partners
from django.utils.html import format_html
from projects.models import ContractsInfo


class Techsupport(models.Model):
    """技术管理总表"""

    # 收样信息
    receive_date = models.DateField(
        verbose_name="收样日期", blank=True, null=True)
    sampling_date = models.DateField(
        verbose_name="采样日期", blank=True, null=True)
    report_end_date = models.DateField(
        verbose_name="报告截止", blank=True, null=True)
    project_source = models.CharField(max_length=50, verbose_name="检测项目来源",
                                      blank=True, null=True)
    send_number = models.CharField(
        max_length=200, verbose_name="快递单号", blank=True, null=True)
    index_number = models.CharField(
        max_length=30, verbose_name="盒子编号", blank=True, null=True)
    report_date = models.DateField(
        verbose_name="报告出具日期", blank=True, null=True)
    pe_number = models.CharField(
        max_length=200, verbose_name="体检号", blank=True, null=True)
    bar_code = models.CharField(
        max_length=50, verbose_name="条形码", blank=True, null=True)
    name = models.CharField(
        max_length=50, verbose_name="姓名", blank=True, null=True)
    gender = models.CharField(
        max_length=50, verbose_name="性别", blank=True, null=True)
    age = models.CharField(
        max_length=50, verbose_name="年龄", blank=True, null=True)
    contact = models.CharField(
        max_length=50, verbose_name="联系方式", blank=True, null=True)
    id_number = models.CharField(
        max_length=50, verbose_name="身份证号码", blank=True, null=True)
    email = models.EmailField(
        verbose_name="邮箱", blank=True, null=True)
    occupation = models.CharField(
        max_length=50, verbose_name="职业", blank=True, null=True)
    bmi = models.CharField(
        max_length=50, verbose_name="BMI", blank=True, null=True)
    height = models.CharField(
        max_length=50, verbose_name="身高(m)", blank=True, null=True)
    weight = models.CharField(
        max_length=50, verbose_name="体重(Kg)", blank=True, null=True)
    note = models.CharField(
        max_length=50, verbose_name="备注", blank=True, null=True)

    # 检测结果
    hemoglobin = models.CharField(
        verbose_name="血红蛋白", max_length=50, blank=True, null=True)
    results = models.CharField(
        verbose_name="综合结果", max_length=200, blank=True, null=True)
    detection_state = models.CharField(
        verbose_name="检测状态", max_length=200, blank=True, null=True)
    register_date = models.DateField(
        verbose_name="登记日期", blank=True, null=True)
    colonoscopy_result = models.CharField(
        verbose_name="肠镜结果", max_length=200, blank=True, null=True)
    # 调查问卷信息
    smoking = models.CharField(
        verbose_name="抽烟", max_length=200, blank=True, null=True)
    drinking = models.CharField(
        verbose_name="喝酒", max_length=200, blank=True, null=True)
    colonoscopy = models.CharField(
        verbose_name="肠镜", max_length=200, blank=True, null=True)
    cancer = models.CharField(
        verbose_name="癌症、息肉史", max_length=200, blank=True, null=True)
    direct_bowel_cancer = models.CharField(
        verbose_name="直系肠癌史", max_length=200, blank=True, null=True)
    lower_digestive = models.CharField(
        verbose_name="下消化道不适症状", max_length=200, blank=True, null=True)
    other_medical_history = models.CharField(
        verbose_name="以下其他病史", max_length=200, blank=True, null=True)
    other_chronic_diseases = models.CharField(
        verbose_name="其他慢性病", max_length=200, blank=True, null=True)
    questionnaire_note = models.CharField(
        verbose_name="调查问卷备注", max_length=200, blank=True, null=True)


class SampleSource(models.Model):
    receive_date = models.OneToOneField(
        verbose_name="收样日期", blank=True, null=True)
    sampling_date = models.DateField(
        verbose_name="采样日期", blank=True, null=True)
    report_end_date = models.DateField(
        verbose_name="报告截止", blank=True, null=True)
    project_source = models.CharField(max_length=50, verbose_name="检测项目来源",
                                      blank=True, null=True)


class BoxDeliveries(models.Model):
    """盒子发货管理"""
    index_number = models.CharField("盒子发货编号", max_length=20)
    sale_man = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="业务员", on_delete=models.SET_NULL,
        null=True)
    customer = models.CharField(max_length=20, verbose_name="客户")
    # box_number = models.IntegerField(verbose_name="邮寄盒子数")
    send_number = models.CharField(max_length=200, verbose_name="快递单号")
    address = models.CharField(max_length=200, verbose_name="地址", default="")
    send_date = models.DateField("邮寄日期", null=True)
    made_date = models.DateField("生产日期", null=True)
    submit = models.BooleanField(verbose_name='提交', default=False)
    parent = models.ForeignKey(
                    Partners, verbose_name="合作方", on_delete=models.SET_NULL,
                    null=True, blank=True)

    class Meta:
        app_label = "tech_support"
        verbose_name = verbose_name_plural = "盒子发货管理"

    def __str__(self):
        return self.index_number


class Boxes(models.Model):
    """盒子管理"""
    BOX_STATUS = (
        (0, '技术支持已发货'),
        (1, '实验已核对'),
        (2, '待提取'),
        (3, '提取中'),
        (4, '待质检'),
        (5, '质检中'),
        (6, '待BS'),
        (7, 'BS中'),
        (8, '待荧光定量'),
        (9, '荧光定量中'),
        (10, '荧光定量完成，结果待审核'),
        (11, '报告已发送'),
    )
    index_number = models.CharField(max_length=30, verbose_name="盒子编号")
    sample_photo = models.FileField('样品照片', upload_to='samplephoto/%Y/%m',
                                    null=True, blank=True)
    box_deliver = models.ForeignKey(
            BoxDeliveries, verbose_name="盒子发货", on_delete=models.SET_NULL,
            null=True, blank=True)
    status = models.IntegerField(choices=BOX_STATUS, verbose_name="盒子状态",
                                 default=1, blank=True, null=True)
    bar_code = models.CharField(max_length=50, verbose_name="条形码")
    name = models.CharField(max_length=20, verbose_name="患者姓名",
                            blank=True, null=True)
    type = models.CharField(
        max_length=20, verbose_name="样本类型", default="粪便",
        blank=True, null=True
    )
    project_source = models.CharField(max_length=50, verbose_name="检测项目来源",
                                      blank=True, null=True)
    is_danger = models.BooleanField(verbose_name="是否高危样品", default=False)
    picking_interval = models.CharField(max_length=20, verbose_name="采收间隔",
                                        blank=True, null=True)
    report_date = models.DateField("报告日期", null=True, blank=True)
    istasking = models.BooleanField(verbose_name="是否开始任务",default=False)

    class Meta:
        app_label = "tech_support"
        verbose_name = verbose_name_plural = "盒子管理"

    def __str__(self):
        return self.index_number


class ExtMethod(models.Model):
    """提取方法管理"""
    method = models.CharField(max_length=30, verbose_name="提取方法")

    class Meta:
        app_label = "tech_support"
        verbose_name = verbose_name_plural = "提取方法管理"

    def __str__(self):
        return self.method


class ExtSubmit(models.Model):
    """提取下单管理"""
    extsubmit_number = models.CharField("提取下单编号", max_length=50)
    boxes = models.ManyToManyField(Boxes, verbose_name="对应盒子信息",)
    exp_method = models.ForeignKey(ExtMethod, verbose_name="提取方法",
                                   on_delete=models.SET_NULL, null=True)
    submit = models.BooleanField(verbose_name='提交', default=False)

    class Meta:
        app_label = "tech_support"
        verbose_name = verbose_name_plural = "提取下单管理"

    def __str__(self):
        return self.extsubmit_number


# class BoxApplications(models.Model):
#     CLASSIFICATION = (
#         ('YY', u'已有合同'),
#         ('YX', u'意向合同'),
#         ('LS', u'零售'),
#         ('ZS', u'赠送')
#     )
#     intention_client = models.ForeignKey(
#         Partners, verbose_name="客户", on_delete=models.SET_NULL, null=True,
#         blank=True
#     )
#     amount = models.IntegerField(
#         verbose_name="申请数量", null=True, blank=True
#     )
#     classification = models.CharField(
#         verbose_name="申请类别", max_length=3, choices=CLASSIFICATION,
#         null=True, blank=True
#     )
#     contract_number = models.ForeignKey(
#         ContractsInfo, verbose_name="合同号", on_delete=models.SET_NULL,
#         null=True, blank=True
#     )
#     address_name = models.CharField(
#         verbose_name="收件人姓名", max_length=50, null=True, blank=True
#     )
#     address_phone = models.CharField(
#         verbose_name="收件人号码", max_length=20, null=True, blank=True
#     )
#     send_address = models.CharField(
#         verbose_name="邮寄地址", max_length=200, null=True, blank=True
#     )
#     submit_time = models.DateField(
#         verbose_name="提交时间", auto_now=True
#     )
#     approval_status = models.BooleanField(
#         verbose_name="审批状态", default=False, null=True, blank=True
#     )
#     box_price = models.FloatField(
#         verbose_name="盒子单价", null=True, blank=True
#     )
#     detection_price = models.FloatField(
#         verbose_name="检测单价", null=True, blank=True
#     )
#     use = models.CharField(
#         verbose_name="用途", max_length=100, null=True, blank=True
#     )
#     proposer = models.ForeignKey(
#         AUTH_USER_MODEL, verbose_name="申请人", on_delete=models.SET_NULL,
#         null=True, blank=True
#     )
#     box_submit_flag = models.BooleanField(
#         verbose_name="是否提交", default=False
#     )
#
#     def colored_contract_number(self):
#         if self.contract_number is not None:
#             if self.contract_number.contract_type == 'YX':
#                 return format_html(
#                     '<span style="color:{}">{}</span>', 'red',
#                     self.contract_number
#                 )
#             return format_html(
#                 '<span>{}</span>', self.contract_number
#             )
#     colored_contract_number.short_description = "合同号"
#
#     class Meta:
#         verbose_name = verbose_name_plural = "盒子申请"
#         ordering = ["-submit_time"]
#
#     def __str__(self):
#         return '盒子申请编号：{}'.format(self.id)


