from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, DateWidget
from tech_support.models import Boxes, BoxDeliveries\
    # , BoxApplications
import datetime
from projects.models import ContractsInfo
from import_export.widgets import IntegerWidget

from tech_support.models_new import Techsupport

Monthchoose = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G",
               8: "H", 9: "I", 10: "G", 11: "K", 12: "L", }


class BoxesResource(resources.ModelResource):
    id = Field(
        column_name='盒子编号', attribute='id', default=None
    )
    deliver_number = Field(
        column_name="盒子发货编号", attribute="box_deliver__index_number")
    bar_code = Field(
        column_name="盒子条形码", attribute="bar_code"
    )

    class Meta:
        model = Boxes
        skip_unchanged = True
        # import_id_fields = ('bar_code',)
        fields = ('id', 'deliver_number', 'bar_code')
        export_order = ('id', 'deliver_number', 'bar_code')

    def export(self, queryset=None, *args, **kwargs):
        queryset_result = Boxes.objects.filter(id=None)
        for i in queryset:
            queryset_result |= Boxes.objects.filter(box_deliver=i)
        return super().export(queryset=queryset_result, *args, **kwargs)

    def get_export_headers(self):
        return ["盒子编号", "盒子发货编号", "盒子条形码"]

    def dehydrate_deliver_number(self, boxes):
        return boxes.box_deliver.index_number

    def init_instance(self, row=None):
        sj = datetime.datetime.now()
        if not row:
            row = {}
        instance = Boxes()
        for attr, value in row.items():
            setattr(instance, attr, value)
        if Boxes.objects.all().count() == 0:
            instance.id = "1"
            instance.index_number = "HZ" + str(sj.year) + \
                                    Monthchoose[
                                        sj.month] + "1"
        else:
            instance.id = str(int(Boxes.objects.latest('id').id) + 1)
            instance.index_number = "HZ" + str(sj.year) + \
                                    Monthchoose[
                                        sj.month] + str(
                Boxes.objects.latest('id').id + 1)
        instance.box_deliver = BoxDeliveries.objects.get(
            index_number=row["盒子发货编号"])

        instance.bar_code = row["盒子条形码"]
        return instance


class TechsupportResources(resources.ModelResource):
    id = Field(
        column_name='id', attribute='id', default=None
    )
    receive_date = Field(
        column_name='收样日期', attribute='receive_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None
    )
    sampling_date = Field(
        column_name='采样日期', attribute='sampling_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None
    )
    report_end_date = Field(
        column_name='报告截止', attribute='report_end_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None
    )
    project_source = Field(
        column_name='检测项目来源', attribute='project_source', default=None
    )
    send_number = Field(
        column_name='快递单号', attribute='send_number', default=None
    )
    index_number = Field(
        column_name='盒子编号', attribute='index_number', default=None
    )
    report_date = Field(
        column_name='报告出具日期', attribute='report_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None
    )
    pe_number = Field(
        column_name='体检号', attribute='pe_number', default=None
    )
    bar_code = Field(
        column_name='条形码', attribute='bar_code', default=None
    )
    name = Field(
        column_name='姓名', attribute='name', default=None
    )
    gender = Field(
        column_name='性别', attribute='gender', default=None
    )
    age = Field(
        column_name='年龄', attribute='age', default=None
    )
    contact = Field(
        column_name='联系方式', attribute='contact', default=None
    )
    id_number = Field(
        column_name='身份证号码', attribute='id_number',
        widget=DateWidget(format='%Y-%m-%d'), default=None
    )
    email = Field(
        column_name='提取-实验备注', attribute='email', default=None
    )
    occupation = Field(
        column_name='职业', attribute='occupation', default=None
    )
    bmi = Field(
        column_name='BMI', attribute='bmi', default=None
    )
    height = Field(
        column_name='身高(m)', attribute='height', default=None
    )
    weight = Field(
        column_name='体重(Kg)', attribute='weight', default=None
    )
    note = Field(
        column_name='备注', attribute='note', default=None
    )
    hemoglobin = Field(
        column_name='血红蛋白', attribute='hemoglobin', default=None
    )
    results = Field(
        column_name='综合结果', attribute='results', default=None
    )
    detection_state = Field(
        column_name='检测状态', attribute='detection_state', default=None
    )
    register_date = Field(
        column_name='登记日期', attribute='register_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None
    )
    colonoscopy_result = Field(
        column_name='肠镜结果', attribute='colonoscopy_result', default=None
    )
    smoking = Field(
        column_name='抽烟', attribute='smoking', default=None
    )
    drinking = Field(
        column_name='喝酒', attribute='drinking', default=None
    )
    colonoscopy = Field(
        column_name='肠镜', attribute='colonoscopy', default=None
    )
    cancer = Field(
        column_name='癌症、息肉史', attribute='cancer', default=None
    )
    direct_bowel_cancer = Field(
        column_name='直系肠癌史', attribute='direct_bowel_cancer', default=None
    )
    lower_digestive = Field(
        column_name='下消化道不适症状', attribute='lower_digestive',
        default=None
    )
    other_medical_history = Field(
        column_name='以下其他病史', attribute='other_medical_history',
        default=None
    )
    other_chronic_diseases = Field(
        column_name='其他慢性病', attribute='other_chronic_diseases',
        widget=DateWidget(format='%Y-%m-%d'), default=None
    )
    questionnaire_note = Field(
        column_name='调查问卷备注', attribute='questionnaire_note',
        default=None
    )

    class Meta:
        model = Techsupport
        skip_unchanged = True
        import_id_fields = ('index_number',)
        fields = (
            "id",
            'receive_date', 'sampling_date', "report_end_date",
            "project_source",
            "send_number", 'index_number', "report_date",
            "pe_number", "bar_code", 'name', "gender", "age",
            'contact',
            "id_number", 'email', "occupation",
            "bmi", "height", "weight",
            "note", 'hemoglobin', "results",
            "detection_state", "register_date", "colonoscopy_result",
            "smoking", 'drinking', "colonoscopy", "cancer",
            "direct_bowel_cancer", "lower_digestive", "other_medical_history",
            "other_chronic_diseases",
            'questionnaire_note')
        export_order = (
            "id",
            'receive_date', 'sampling_date', "report_end_date",
            "project_source",
            "send_number", 'index_number', "report_date",
            "pe_number", "bar_code", 'name', "gender", "age",
            'contact',
            "id_number", 'email', "occupation",
            "bmi", "height", "weight",
            "note", 'hemoglobin', "results",
            "detection_state", "register_date", "colonoscopy_result",
            "smoking", 'drinking', "colonoscopy", "cancer",
            "direct_bowel_cancer", "lower_digestive", "other_medical_history",
            "other_chronic_diseases",
            'questionnaire_note')

    def get_export_headers(self):
        return ["id", "收样日期", "盒子条形码", "报告截止",
                "检测项目来源", "快递单号", "盒子编号", "报告出具日期",
                "体检号", "条形码", "姓名",
                "性别", "年龄", "联系方式", "身份证号码",
                "邮箱", "职业", "BMI", "身高(m)",
                "体重(Kg)", "备注",
                "血红蛋白", "综合结果",
                "检测状态", "登记日期", "肠镜结果", "抽烟",
                "喝酒", "肠镜", "癌症、息肉史",
                "直系肠癌史", "下消化道不适症状", "以下其他病史", "其他慢性病",
                "调查问卷备注"
                ]




# class BoxApplicationsResources(resources.ModelResource):
#     """盒子申请信息导入导出"""
#
#     application_id = Field(
#         column_name="申请编号", attribute='id', default=None
#     )
#     contract_id = Field(
#         column_name="合同号", attribute='contract_number',
#         widget=ForeignKeyWidget(ContractsInfo, 'contract_number'), default=None
#     )
#     amount = Field(
#         column_name="申请数量", attribute='amount', widget=IntegerWidget()
#     )
#     classification = Field(
#         column_name="申请类别", attribute='classification'
#     )
#     address_name = Field(
#         column_name="收件人姓名", attribute='address_name'
#     )
#     address_phone = Field(
#         column_name="收件人号码", attribute='address_phone'
#     )
#     send_address = Field(
#         column_name="邮寄地址", attribute='send_address'
#     )
#     box_price = Field(
#         column_name="盒子单价", attribute='box_price', default=None
#     )
#     detection_price = Field(
#         column_name="检测单价", attribute='detection_price', default=None
#     )
#     use = Field(
#         column_name="用途", attribute='use'
#     )
#     proposer = Field(
#         column_name="申请人", attribute='proposer', default=None
#     )
#     submit_time = Field(
#         column_name="提交时间", attribute='submit_time', widget=DateWidget(
#             '%Y-%m-%d')
#     )
#     approval_status = Field(
#         column_name="审批状态", attribute='approval_status'
#     )
#     box_submit_flag = Field(
#         column_name="是否提交", attribute='box_submit_flag'
#     )
#
#     class Meta:
#         model = BoxApplications
#         fields = (
#             'application_id', 'contract_id', 'amount', 'classification',
#             'address_name', 'address_phone', 'send_address', 'box_price',
#             'detection_price', 'use', 'proposer', 'submit_time',
#             'approval_status', 'box_submit_flag'
#         )
#         export_order = (
#             'application_id', 'contract_id', 'amount', 'classification',
#             'address_name', 'address_phone', 'send_address', 'box_price',
#             'detection_price', 'use', 'proposer', 'submit_time',
#             'approval_status', 'box_submit_flag'
#         )
#         skip_unchanged = True
#         import_id_fields = ['application_id']
#
#     def get_export_headers(self):
#         export_headers = [u'申请编号', u'合同号', u'申请数量', u'申请类别',
#                           u'收件人姓名', u'收件人号码', u'邮寄地址', u'盒子单价',
#                           u'检测单价', u'用途', u'申请人', u'提交时间', u'审批状态',
#                           u'是否提交']
#         return export_headers
