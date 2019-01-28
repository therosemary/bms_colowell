from django.db import models
from bms_colowell.settings import AUTH_USER_MODEL


class BoxDeliveries(models.Model):
    """盒子发货管理"""
    index_number = models.CharField("盒子发货编号", max_length=20)
    sale_man = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="业务员", on_delete=models.SET_NULL,
        null=True)
    customer = models.CharField(max_length=20, verbose_name="客户")
    box_number = models.IntegerField(verbose_name="邮寄盒子数")
    send_number = models.CharField(max_length=200, verbose_name="快递单号信息")
    send_date = models.DateField("邮寄日期", null=True)
    made_date = models.DateField("生产日期", null=True)
    submit = models.BooleanField(verbose_name='提交', default=False)

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
        (3, '提取完成，待质检'),
        (4, '质检完成，待BS'),
        (5, 'BS完成，待荧光定量'),
        (6, '荧光定量完成，结果待审核'),
        (7, '报告已发送'),
    )
    index_number = models.CharField(max_length=30, verbose_name="盒子编号")
    sample_photo = models.FileField('样品照片', upload_to='samplephoto/%Y/%m',
                                    null=True, blank=True)
    box_deliver = models.ForeignKey(BoxDeliveries, verbose_name="盒子发货",
                                    on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=BOX_STATUS, verbose_name="盒子状态",
                                 default=1, blank=True, null=True)
    bar_code = models.CharField(max_length=50, verbose_name="条形码")
    name = models.CharField(max_length=20, verbose_name="患者姓名")
    type = models.CharField(
        max_length=20, verbose_name="样本类型", default="粪便"
    )
    projec_source = models.CharField(max_length=50, verbose_name="检测项目来源")
    is_danger = models.BooleanField(verbose_name="是否高危样品")
    picking_interval = models.CharField(max_length=20, verbose_name="采收间隔")
    report_date = models.DateField("报告日期", null=True)

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
    boxes = models.ForeignKey(BoxDeliveries, verbose_name="对应盒子信息",
                              on_delete=models.SET_NULL, null=True)
    exp_method = models.ForeignKey(ExtMethod, verbose_name="提取方法",
                                   on_delete=models.SET_NULL, null=True)
    submit = models.BooleanField(verbose_name='提交', default=False)

    class Meta:
        app_label = "tech_support"
        verbose_name = verbose_name_plural = "提取下单管理"

    def __str__(self):
        return self.extsubmit_number
