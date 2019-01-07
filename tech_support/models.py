from django.db import models
from bms_colowell.settings import AUTH_USER_MODEL
# Create your models here.


class BoxDeliveries(models.Model):
    index_number = models.CharField("盒子发货编号",max_length=20)
    sale_man = models.ForeignKey(AUTH_USER_MODEL,verbose_name="业务员",on_delete=models.SET_NULL,null=True)
    customer = models.CharField(max_length=20,verbose_name="客户")
    box_number = models.IntegerField(verbose_name="邮寄盒子数")
    send_number = models.CharField(max_length=200,verbose_name="快递单号信息")
    send_date = models.DateField("邮寄日期", null=True)
    made_date = models.DateField("生产日期",null=True)

class Boxes(models.Model):
    Box_Status = (
        (1, '待提取'),
        (2, '提取完成，待质检'),
        (3, '质检完成，待BS'),
        (4, 'BS完成，待荧光定量'),
        (5, '荧光定量完成，结果待审核'),
        (6, '报告已发送'),
    )
    index_number = models.CharField(max_length=30,verbose_name="盒子编号")
    sample_photo = models.FileField('样品照片', upload_to='samplephoto/%Y/%m', null=True, blank=True)
    box_deliver = models.ForeignKey(BoxDeliveries,verbose_name="盒子发货",on_delete=models.SET_NULL,null=True)
    status = models.IntegerField(choices=Box_Status,verbose_name="盒子状态",default=1)
    bar_code = models.CharField(max_length=50,verbose_name="条形码")
    name = models.CharField(max_length=20,verbose_name="患者姓名")
    type = models.CharField(max_length=20,verbose_name="样本类型",default="粪便")
    projec_source = models.CharField(max_length=50,verbose_name="检测项目来源")
    is_danger = models.BooleanField(verbose_name="是否高危样品")
    picking_interval = models.CharField(max_length=20,verbose_name="采收间隔")
    report_date = models.DateField("报告日期",null=True)


class ExtMethod(models.Model):
    method = models.CharField(max_length=30,verbose_name="提取方法")

class ExtSubmit(models.Model):
    extsubmit_number = models.CharField("提取下单编号",max_length=50)
    boxes = models.ForeignKey(BoxDeliveries,verbose_name="对应盒子信息",on_delete=models.SET_NULL,null=True)
    exp_method = models.ForeignKey(ExtMethod,verbose_name="提取方法",on_delete=models.SET_NULL,null=True)
