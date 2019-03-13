from import_export import resources
from accounts.models import BmsUser
from experiments.models import Experiments
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, DateWidget

from tech_support.models import Boxes


class ExperimentsResource(resources.ModelResource):
    id = Field(
        column_name='id', attribute='id', default=None
    )
    index_number = Field(
        column_name='实验编号', attribute='index_number', default=None
    )
    boxes = Field(
        column_name='盒子条形码', attribute='boxes',
        widget=ForeignKeyWidget(Boxes, "index_number"), default=None
    )
    receive_date = Field(
        column_name='收样日期', attribute='receive_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None
    )
    projects_source = Field(
        column_name='检测项目来源', attribute='projects_source', default=None
    )
    ext_method = Field(
        column_name='提取-提取方法', attribute='ext_method', default=None
    )
    ext_objective = Field(
        column_name='提取-目的', attribute='ext_objective', default=None
    )
    ext_start_number = Field(
        column_name='提取-起始取样量(ml)', attribute='ext_start_number',
        default=None
    )
    ext_hemoglobin = Field(
        column_name='提取-血红蛋白', attribute='ext_hemoglobin',
        default=None
    )
    ext_cz_volume = Field(
        column_name='提取-磁珠体积(ul)', attribute='ext_cz_volume',
        default=None
    )
    ext_density = Field(
        column_name='提取-提取浓度(ng/ul)', attribute='ext_density',
        default=None
    )
    ext_elution_volume = Field(
        column_name='提取-洗脱体积(ul)', attribute='ext_elution_volume',
        default=None
    )
    ext_operator = Field(
        column_name='提取-操作人员', attribute='ext_operator',
        widget=ForeignKeyWidget(BmsUser, "username"),
        default=None
    )
    ext_date = Field(
        column_name='提取-日期', attribute='ext_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None
    )
    ext_note = Field(
        column_name='提取-实验备注', attribute='ext_note',
        default=None
    )
    qua_test_number = Field(
        column_name='质检-试剂批次', attribute='qua_test_number',
        default=None
    )
    qua_instrument = Field(
        column_name='质检-仪器', attribute='qua_instrument',
        default=None
    )
    qua_sample_size = Field(
        column_name='质检-上样量', attribute='qua_sample_size',
        default=None
    )
    qua_loop_number = Field(
        column_name='质检-循环数', attribute='qua_loop_number',
        default=None
    )
    qua_background = Field(
        column_name='质检-Background', attribute='qua_background',
        default=None
    )
    qua_noise = Field(
        column_name='质检-非甲基化内参ACTB_Noise Band', attribute='qua_noise',
        default=None
    )
    qua_ct = Field(
        column_name='质检-非甲基化内参ACTB_CT值', attribute='qua_ct',
        default=None
    )
    qua_amplification_curve = Field(
        column_name='质检-非甲基化内参ACTB_扩增曲线',
        attribute='qua_amplification_curve',
        default=None
    )
    qua_is_quality = Field(
        column_name='质检-有无质控', attribute='qua_is_quality',
        default=None
    )
    qua_operator = Field(
        column_name='质检-操作人员', attribute='qua_operator',
        widget=ForeignKeyWidget(BmsUser, "username"),
        default=None
    )
    qua_date = Field(
        column_name='质检-日期', attribute='qua_date',
        widget=DateWidget(format='%Y-%m-%d'),
        default=None
    )
    qua_note = Field(
        column_name='质检-实验备注', attribute='qua_note',
        default=None
    )
    bis_test_number = Field(
        column_name='BIS-试剂批次', attribute='bis_test_number',
        default=None
    )
    bis_begin = Field(
        column_name='BIS-起始量(ng)', attribute='bis_begin',
        default=None
    )
    bis_template = Field(
        column_name='BIS-模板量(ul)', attribute='bis_template',
        default=None
    )
    bis_elution = Field(
        column_name='BIS-洗脱体积(ul)', attribute='bis_elution',
        default=None
    )
    bis_is_quality = Field(
        column_name='BIS-有无质控', attribute='bis_is_quality',
        default=None
    )
    bis_date = Field(
        column_name='BIS-日期', attribute='bis_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None
    )
    bis_operator = Field(
        column_name='BIS-操作人员', attribute='bis_operator',
        widget=ForeignKeyWidget(BmsUser, "username"),
        default=None
    )
    bis_note = Field(
        column_name='BIS-实验备注', attribute='bis_note',
        default=None
    )
    fq_test_number = Field(
        column_name='荧光定量-试剂批次', attribute='fq_test_number',
        default=None
    )
    fq_instrument = Field(
        column_name='荧光定量-仪器', attribute='fq_instrument',
        default=None
    )
    fq_loop_number = Field(
        column_name='荧光定量-循环数', attribute='fq_loop_number',
        default=None
    )
    fq_background = Field(
        column_name='荧光定量-Background', attribute='fq_background',
        default=None
    )
    fq_actb_noise = Field(
        column_name='荧光定量-ACTB_NoiseBand/STDMultiplier',
        attribute='fq_actb_noise',
        default=None
    )
    fq_actb_ct = Field(
        column_name='荧光定量-ACTB_CT值', attribute='fq_actb_ct',
        default=None
    )
    fq_actb_amp = Field(
        column_name='荧光定量-ACTB_扩增曲线', attribute='fq_actb_amp',
        default=None
    )
    fq_sfrp2_noise = Field(
        column_name='荧光定量-Sfrp2_NoiseBand/STDMultiplier',
        attribute='fq_sfrp2_noise',
        default=None
    )
    fq_sfrp2_ct = Field(
        column_name='荧光定量-Sfrp2_CT值', attribute='fq_sfrp2_ct',
        default=None
    )
    fq_sfrp2_amp = Field(
        column_name='荧光定量-Sfrp2_扩增曲线', attribute='fq_sfrp2_amp',
        default=None
    )
    fq_sdc2_noise = Field(
        column_name='荧光定量-Sdc2_NoiseBand/STDMultiplier',
        attribute='fq_sdc2_noise',
        default=None
    )
    fq_sdc2_ct = Field(
        column_name='荧光定量-Sdc2_CT值', attribute='fq_sdc2_ct',
        default=None
    )
    fq_sdc2_amp = Field(
        column_name='荧光定量-Sdc2_扩增曲线', attribute='fq_sdc2_amp',
        default=None
    )
    fq_is_quality = Field(
        column_name='荧光定量-有无质控', attribute='fq_is_quality',
        default=None
    )
    fq_operator = Field(
        column_name='荧光定量-操作人员', attribute='fq_operator',
        widget=ForeignKeyWidget(BmsUser, "username"),
        default=None
    )
    fq_date = Field(
        column_name='荧光定量-日期', attribute='fq_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None
    )
    fq_suggest = Field(
        column_name='荧光定量-建议', attribute='fq_suggest',
        default=None
    )

    class Meta:
        model = Experiments
        skip_unchanged = True
        import_id_fields = ('index_number',)
        fields = (
                  "id",
                  'index_number', 'boxes', "receive_date", "projects_source",
                  "ext_method", 'ext_objective', "ext_start_number",
                  "ext_hemoglobin", "ext_cz_volume", 'ext_density',
                  "ext_elution_volume", "ext_operator", 'ext_date',
                  "ext_note", 'qua_test_number', "qua_instrument",
                  "qua_sample_size", "qua_loop_number", "qua_background",
                  "qua_noise", 'qua_ct', "qua_amplification_curve",
                  "qua_is_quality", "qua_operator", "qua_date",
                  "qua_note", 'bis_test_number', "bis_begin", "bis_template",
                  "bis_elution", "bis_is_quality", "bis_operator", "bis_date",
                  'bis_note',
                  'fq_test_number', "fq_instrument", "fq_loop_number",
                  "fq_background", "fq_actb_noise", 'fq_actb_ct',
                  "fq_actb_amp", "fq_sfrp2_noise", 'fq_sfrp2_ct',
                  "fq_sfrp2_amp", "fq_sdc2_noise", 'fq_sdc2_ct', "fq_sdc2_amp",
                  "fq_is_quality", "fq_operator", "fq_date", "fq_suggest")
        export_order = (
                  "id",
                  'index_number', 'boxes', "receive_date", "projects_source",
                  "ext_method", 'ext_objective', "ext_start_number",
                  "ext_hemoglobin", "ext_cz_volume", 'ext_density',
                  "ext_elution_volume", "ext_operator", 'ext_date',
                  "ext_note", 'qua_test_number', "qua_instrument",
                  "qua_sample_size", "qua_loop_number", "qua_background",
                  "qua_noise", 'qua_ct', "qua_amplification_curve",
                  "qua_is_quality", "qua_operator", "qua_date",
                  "qua_note", 'bis_test_number', "bis_begin", "bis_template",
                  "bis_elution", "bis_is_quality", "bis_operator", "bis_date",
                  'bis_note',
                  'fq_test_number', "fq_instrument", "fq_loop_number",
                  "fq_background", "fq_actb_noise", 'fq_actb_ct',
                  "fq_actb_amp", "fq_sfrp2_noise", 'fq_sfrp2_ct',
                  "fq_sfrp2_amp", "fq_sdc2_noise", 'fq_sdc2_ct', "fq_sdc2_amp",
                  "fq_is_quality", "fq_operator", "fq_date", "fq_suggest")

    def get_export_headers(self):
        return ["id", "实验编号", "盒子条形码", "收样日期",
                "检测项目来源", "提取-提取方法", "提取-目的", "提取-起始取样量(ml)",
                "提取-血红蛋白", "提取-磁珠体积(ul)", "提取-提取浓度(ng/ul)",
                "提取-洗脱体积(ul)", "提取-操作人员", "提取-日期", "提取-实验备注",
                "质检-试剂批次", "质检-仪器", "质检-上样量", "质检-循环数",
                "质检-Background", "质检-非甲基化内参ACTB_Noise Band",
                "质检-非甲基化内参ACTB_CT值", "质检-非甲基化内参ACTB_扩增曲线",
                "质检-有无质控", "质检-操作人员", "质检-日期", "质检-实验备注",
                "BIS-试剂批次", "BIS-起始量(ng)", "BIS-模板量(ul)",
                "BIS-洗脱体积(ul)", "BIS-有无质控", "BIS-操作人员", "BIS-日期",
                "BIS-实验备注", "荧光定量-试剂批次", "荧光定量-仪器",
                "荧光定量-循环数", "荧光定量-Background",
                "荧光定量-ACTB_NoiseBand/STDMultiplier", "荧光定量-ACTB_CT值",
                "荧光定量-ACTB_扩增曲线",
                "荧光定量-Sfrp2_NoiseBand/STDMultiplier",'荧光定量-Sfrp2_CT值',
                '荧光定量-Sfrp2_扩增曲线',
                '荧光定量-Sdc2_NoiseBand/STDMultiplier','荧光定量-Sdc2_CT值',
                '荧光定量-Sdc2_扩增曲线', '荧光定量-有无质控', '荧光定量-操作人员',
                '荧光定量-日期', '荧光定量-建议'
                ]

    # def get_or_init_instance(self, instance_loader, row):
    #     instance = self.get_instance(instance_loader, row)
    #     if instance:
    #         # instance.operator = BmsUser.objects.get(username=row['操作人员'])
    #         instance.test_number = row['试剂批号']
    #         instance.ext_method = row['提取方法']
    #         instance.objective = row['目的']
    #         instance.start_number = row['起始取样量(ml)']
    #         instance.hemoglobin = row['血红蛋白']
    #         instance.cizhutiji = row['磁珠体积(ul)']
    #         instance.ext_density = row['提取浓度(ng/ul)']
    #         instance.elution_volume = row["洗脱体积(ul)"]
    #         # instance.ext_date = row["提取日期"]
    #         instance.note = row["实验异常备注"]
    #         instance.save()
    #         return instance, False
    #     else:
    #         return self.init_instance(row), True
    #
    # def init_instance(self, row=None):
    #     if not row:
    #         row = {}
    #     instance = ExtExecute()
    #     for attr, value in row.items():
    #         setattr(instance, attr, value)
    #     if ExtExecute.objects.all().count() == 0:
    #         instance.id = "1"
    #     else:
    #         instance.id = str(int(ExtExecute.objects.latest('id').id) + 1)
    #     instance.ext_number = row['实验编号']
    #     # instance.operator = BmsUser.objects.get(username=row['操作人员'])
    #     instance.test_number = row['试剂批号']
    #     instance.ext_method = row['提取方法']
    #     instance.objective = row['目的']
    #     instance.start_number = row['起始取样量(ml)']
    #     instance.hemoglobin = row['血红蛋白']
    #     instance.cizhutiji = row['磁珠体积(ul)']
    #     instance.ext_density = row['提取浓度(ng/ul)']
    #     instance.elution_volume = row["洗脱体积(ul)"]
    #     # instance.ext_date = row["提取日期"]
    #     instance.note = row["实验异常备注"]
    #     instance.save()
    #     return instance
