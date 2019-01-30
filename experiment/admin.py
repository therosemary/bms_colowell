import datetime
from import_export.admin import ImportExportActionModelAdmin
from tech_support.models import Boxes
from django.contrib import admin
from accounts.models import BmsUser
from experiment.forms import ExtExecuteForm, QualityTestForm, BsTaskForm, \
    FluorescenceQuantificationForm
from import_export import resources
from experiment.models import *

Monthchoose = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G",
               8: "H", 9: "I", 10: "G", 11: "K", 12: "L", }


class ExtExecuteResource(resources.ModelResource):
    class Meta:
        model = ExtExecute
        skip_unchanged = True
        import_id_fields = 'ext_number'
        fields = ('ext_number', 'operator',
                  'test_number', 'ext_method', "objective", 'start_number',
                  'hemoglobin', 'cizhutiji', 'ext_density', 'elution_volume',
                  "ext_date", "note")
        export_order = ('ext_number', 'operator',
                        'test_number', 'ext_method', "objective",
                        'start_number',
                        'hemoglobin', 'cizhutiji', 'ext_density',
                        'elution_volume',
                        "ext_date", "note")

    def get_export_headers(self):
        return ["实验编号", "操作人员", "试剂批号", "提取方法", "目的",
                "起始取样量(ml)", "血红蛋白", "磁珠体积(ul)", "提取浓度(ng/ul)",
                "洗脱体积(ul)", "提取日期", "实验异常备注"]

    # def get_diff_headers(self):
    #     return ["实验编号", "操作人员", "试剂批号", "提取方法", "目的",
    #             "起始取样量(ml)", "血红蛋白", "磁珠体积(ul)", "提取浓度(ng/ul)",
    #             "洗脱体积(ul)", "提取日期", "实验异常备注"]

    def get_or_init_instance(self, instance_loader, row):
        instance = self.get_instance(instance_loader, row)
        if instance:
            instance.operator = BmsUser.objects.get(username=row['操作人员'])
            instance.test_number = row['试剂批号']
            instance.ext_method = row['提取方法']
            instance.objective = row['目的']
            instance.start_number = row['起始取样量(ml)']
            instance.hemoglobin = row['血红蛋白']
            instance.cizhutiji = row['磁珠体积(ul)']
            instance.ext_density = row['提取浓度(ng/ul)']
            instance.elution_volume = row["洗脱体积(ul)"]
            instance.ext_date = row["提取日期"]
            instance.note = row["实验异常备注"]
            instance.save()
            return instance, False
        else:
            return self.init_instance(row), True

    def init_instance(self, row=None):
        if not row:
            row = {}
        instance = ExtExecute()
        for attr, value in row.items():
            setattr(instance, attr, value)
        if ExtExecute.objects.all().count() == 0:
            instance.id = "1"
        else:
            instance.id = str(int(ExtExecute.objects.latest('id').id) + 1)
        instance.ext_number = row['实验编号']
        instance.operator = BmsUser.objects.get(username=row['操作人员'])
        instance.test_number = row['试剂批号']
        instance.ext_method = row['提取方法']
        instance.objective = row['目的']
        instance.start_number = row['起始取样量(ml)']
        instance.hemoglobin = row['血红蛋白']
        instance.cizhutiji = row['磁珠体积(ul)']
        instance.ext_density = row['提取浓度(ng/ul)']
        instance.elution_volume = row["洗脱体积(ul)"]
        instance.ext_date = row["提取日期"]
        instance.note = row["实验异常备注"]
        instance.save()
        return instance


class ExtExecuteAdmin(ImportExportActionModelAdmin):
    """提取管理"""
    form = ExtExecuteForm
    list_per_page = 50
    search_fields = ('ext_number', "status", "ext_date")
    save_on_top = False
    resource_class = ExtExecuteResource
    list_display = (
        'ext_number', "boxes", "test_number", 'ext_method', 'ext_date',
        'status',
    )
    readonly_fields = ["produce_", "is_qualified"]
    list_display_links = ('ext_number',)
    fieldsets = (
        ('实验相关信息', {
            'fields': ('boxes', 'ext_method', 'ext_times', "operator",
                       "ext_date")
        }),
        ('实验数据', {
            'fields': ("test_number", ('start_number', "hemoglobin"),
                       ("cizhutiji", "ext_density"),
                       ("elution_volume", 'produce_',), "is_qualified")
        }),
        ('实验结果', {
            'fields': ('note',)
        }),
    )

    def produce_(self, obj):
        # try:
        #     pro = float(obj.elution_volume) * float(obj.ext_density)
        # except:
        #     return "数据有误请查看"
        # return pro
        if obj:
            if obj.elution_volume and obj.ext_density:
                pro = float(obj.elution_volume) * float(obj.ext_density)
                return pro
            else:
                return None
        return None

    produce_.short_description = "产出"

    def is_qualified(self, obj):
        if obj:
            if obj.elution_volume and obj.ext_density:
                pro = float(obj.elution_volume) * float(obj.ext_density)
                if pro >= 2:
                    return "合格"
                else:
                    return "不合格"
            else:
                return None
        else:
            return None

    is_qualified.short_description = "是否合格"

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.status == 1 or obj.status == 2:
                self.readonly_fields = ['boxes', 'ext_method', 'ext_times',
                                        "operator", "ext_date", "test_number",
                                        'start_number', "hemoglobin",
                                        "cizhutiji", "ext_density",
                                        "elution_volume", "produce_",
                                        "is_qualified", 'note', ]
                return self.readonly_fields
        except AttributeError:
            self.readonly_fields = ["produce_", "is_qualified"]
            return self.readonly_fields
        self.readonly_fields = ["produce_", "is_qualified"]
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not obj.ext_number:
            box = form.cleaned_data["boxes"]
            query_ext = ExtExecute.objects.filter(boxes=box)
            if query_ext.count() == 1:
                if "_" not in query_ext.first().ext_number:
                    obj.ext_number = query_ext.first().ext_number + "_1"
            elif query_ext.count() > 1:
                index = 0
                for i in query_ext:
                    if "_" in i.ext_number:
                        if index < int(i.ext_number[-1]):
                            index = int(i.ext_number[-1])
                obj.ext_number = query_ext.first().ext_number + "_" + str(
                    index + 1)
            else:
                sj = datetime.datetime.now()
                if ExtExecute.objects.all().count() == 0:
                    obj.ext_number = str(sj.year) + Monthchoose[
                        sj.month] + "1".zfill(5)

                else:
                    obj.ext_number = str(sj.year) + Monthchoose[
                        sj.month] + str(
                        BoxDeliveries.objects.latest('id').id + 1).zfill(5)
        if obj.status == 1:
            QualityTest.objects.create(qua_number=obj.ext_number,
                                       boxes=obj.boxex)
        else:
            pass
        obj.save()


class QualityTestResource(resources.ModelResource):
    class Meta:
        model = QualityTest
        skip_unchanged = True
        import_id_fields = 'qua_number'
        fields = ('qua_number', "operator", 'test_number', 'template_number',
                  'instrument', "loop_number", 'background_baseline', "noise",
                  'ct', 'amplification_curve', 'is_quality', 'qua_date',
                  "note")
        export_order = (
            'qua_number', "operator", 'test_number', 'template_number',
            'instrument', "loop_number", 'background_baseline', "noise",
            'ct', 'amplification_curve', 'is_quality', 'qua_date',
            "note")

    def get_export_headers(self):
        return ["实验编号", "实验人员", "试剂批号", "上样模板量", "仪器", "循环数",
                "Background/Baseline", "非甲基化内参ACTB_Noise Band",
                "非甲基化内参ACTB_CT值", "非甲基化内参ACTB_扩增曲线",
                "有无质控", "质检日期", "实验异常备注"]

    def get_or_init_instance(self, instance_loader, row):
        instance = self.get_instance(instance_loader, row)
        if instance:
            instance.test_number = row['试剂批号']
            instance.template_number = row['上样模板量']
            instance.operator = BmsUser.objects.get(username=row['操作人员'])
            instance.instrument = row['仪器']
            instance.loop_number = row['循环数']
            instance.background_baseline = row['Background/Baseline']
            instance.noise = row['非甲基化内参ACTB_Noise Band']
            instance.ct = row['非甲基化内参ACTB_CT值']
            instance.amplification_curve = row["非甲基化内参ACTB_扩增曲线"]
            instance.is_quality = row["提取日期"]
            instance.qua_date = row["质检日期"]
            instance.note = row["实验异常备注"]
            instance.save()
            return instance, False
        else:
            return self.init_instance(row), True

    def init_instance(self, row=None):
        if not row:
            row = {}
        instance = QualityTest()
        for attr, value in row.items():
            setattr(instance, attr, value)
        if QualityTest.objects.all().count() == 0:
            instance.id = "1"
        else:
            instance.id = str(int(QualityTest.objects.latest('id').id) + 1)
        instance.qua_number = row['实验编号']
        instance.test_number = row['试剂批号']
        instance.operator = BmsUser.objects.get(username=row['操作人员'])
        instance.template_number = row['上样模板量']
        instance.instrument = row['仪器']
        instance.loop_number = row['循环数']
        instance.background_baseline = row['Background/Baseline']
        instance.noise = row['非甲基化内参ACTB_Noise Band']
        instance.ct = row['非甲基化内参ACTB_CT值']
        instance.amplification_curve = row["非甲基化内参ACTB_扩增曲线"]
        instance.is_quality = row["提取日期"]
        instance.qua_date = row["质检日期"]
        instance.note = row["实验异常备注"]
        instance.save()
        return instance


class QualityTestAdmin(ImportExportActionModelAdmin):
    """质检管理"""
    list_per_page = 50
    search_fields = ('qua_number', "status", "qua_date")
    save_on_top = False
    list_display = (
        'qua_number', "boxes", 'test_number', 'operator', 'qua_date',
        "status",
    )
    resource_class = QualityTestResource
    list_display_links = ('qua_number',)
    form = QualityTestForm
    fieldsets = (
        ('实验相关信息', {
            'fields': ('boxes', "operator", "qua_date")
        }),
        ('实验数据', {
            'fields': ("test_number", ("instrument", 'template_number'),
                       ("loop_number", "background_baseline"))
        }),
        ('非甲基化ACTB', {
            'fields': ("ct", "amplification_curve", "threshold_line")
        }),
        ('实验结果', {
            'fields': ('note',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.status == 1 or obj.status == 2:
                self.readonly_fields = ['boxes', "operator", "qua_date",
                                        "test_number", "instrument",
                                        'template_number', "loop_number",
                                        "background_baseline", "ct",
                                        "amplification_curve",
                                        'note', "threshold_line"]
                return self.readonly_fields
        except AttributeError:
            self.readonly_fields = []
            return self.readonly_fields
        self.readonly_fields = []
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.status == 1:
            BsTask.objects.create(bs_number=obj.qua_number,
                                  boxes=obj.boxex)
        else:
            pass
        obj.save()


class BsTaskResource(resources.ModelResource):
    class Meta:
        model = BsTask
        skip_unchanged = True
        import_id_fields = 'bs_number'
        fields = ('bs_number', "operator", 'test_number', 'bis_begin',
                  'bis_template', "bis_elution", 'is_quality', "operator",
                  'bs_date', 'note')
        export_order = (
            'bs_number', "operator", 'test_number', 'bis_begin',
            'bis_template', "bis_elution", 'is_quality', "operator",
            'bs_date', 'note')

    def get_export_headers(self):
        return ["实验编号", "试剂批号", "BIS起始量(ng)", "BIS模板量(ul)",
                "BIS洗脱体积(ul)",
                "有无质控", "操作人员",
                "BS实验日期", "实验异常备注"]

    def get_or_init_instance(self, instance_loader, row):
        instance = self.get_instance(instance_loader, row)
        if instance:
            instance.test_number = row['试剂批号']
            instance.bis_begin = row['BIS起始量(ng)']
            instance.bis_template = row['BIS模板量(ul)']
            instance.bis_elution = row['BIS洗脱体积(ul)']
            instance.is_quality = row['有无质控']
            instance.operator = BmsUser.objects.get(username=row['操作人员'])
            instance.bs_date = row['BS实验日期']
            instance.note = row["实验异常备注"]
            instance.save()
            return instance, False
        else:
            return self.init_instance(row), True

    def init_instance(self, row=None):
        if not row:
            row = {}
        instance = QualityTest()
        for attr, value in row.items():
            setattr(instance, attr, value)
        if BsTask.objects.all().count() == 0:
            instance.id = "1"
        else:
            instance.id = str(int(BsTask.objects.latest('id').id) + 1)
        instance.bs_number = row['实验编号']
        instance.test_number = row['试剂批号']
        instance.bis_begin = row['BIS起始量(ng)']
        instance.bis_template = row['BIS模板量(ul)']
        instance.bis_elution = row['BIS洗脱体积(ul)']
        instance.is_quality = row['有无质控']
        instance.operator = BmsUser.objects.get(username=row['操作人员'])
        instance.bs_date = row['BS实验日期']
        instance.note = row["实验异常备注"]
        instance.save()
        return instance


class BsTaskAdmin(ImportExportActionModelAdmin):
    """BS管理"""
    list_per_page = 50
    search_fields = ("status", "bs_date")
    save_on_top = False
    list_display = (
        'bs_number', "boxes", 'test_number', "bs_times", 'operator', 'bs_date',
        "status",
    )
    resource_class = BsTaskResource
    list_display_links = ('bs_number',)
    form = BsTaskForm
    fieldsets = (
        ('实验相关信息', {
            'fields': ('boxes', "operator", "bs_times", "bs_date")
        }),
        ('实验数据', {
            'fields': ("test_number", ("bis_begin", 'bis_template'),
                       ("bis_elution", "is_quality"))
        }),
        ('实验结果', {
            'fields': ('note',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.status == 1 or obj.status == 2:
                self.readonly_fields = ['boxes', "operator", "bs_times",
                                        "bs_date", "test_number", "bis_begin",
                                        'bis_template', "bis_elution", 'note',
                                        "is_quality", ]
                return self.readonly_fields
        except AttributeError:
            self.readonly_fields = []
            return self.readonly_fields
        self.readonly_fields = []
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.status == 1:
            FluorescenceQuantification.objects.create(fq_number=obj.bs_number,
                                                      boxes=obj.boxex)
        else:
            pass
        obj.save()


class FluorescenceQuantificationResource(resources.ModelResource):
    class Meta:
        model = FluorescenceQuantification
        skip_unchanged = True
        import_id_fields = 'fq_number'
        fields = ('fq_number', 'test_number', 'instrument', 'loop_number',
                  "background", 'actb_noise', "actb_ct", "actb_amp",
                  "sfrp2_noise", "sfrp2_ct", "sfrp2_amp", 'sdc2_noise',
                  'sdc2_ct', "sdc2_amp", "is_quality", "operator", "fq_date")
        export_order = (
            'fq_number', 'test_number', 'instrument', 'loop_number',
            "background", 'actb_noise', "actb_ct", "actb_amp",
            "sfrp2_noise", "sfrp2_ct", "sfrp2_amp", 'sdc2_noise',
            'sdc2_ct', "sdc2_amp", "is_quality", "operator", "fq_date")

    def get_export_headers(self):
        return ["实验编号", "试剂批号", "仪器", "循环数", "background",
                'actb_noise', "actb_ct", "actb_amp",
                "sfrp2_noise", "sfrp2_ct", "sfrp2_amp", 'sdc2_noise',
                'sdc2_ct', "sdc2_amp",
                "有无质控", "操作人员",
                "荧光定量日期"]

    def get_or_init_instance(self, instance_loader, row):
        instance = self.get_instance(instance_loader, row)
        if instance:
            instance.test_number = row['试剂批号']
            instance.bis_begin = row['BIS起始量(ng)']
            instance.bis_template = row['BIS模板量(ul)']
            instance.bis_elution = row['BIS洗脱体积(ul)']
            instance.is_quality = row['有无质控']
            instance.operator = BmsUser.objects.get(username=row['操作人员'])
            instance.bs_date = row['BS实验日期']
            instance.note = row["实验异常备注"]
            instance.save()
            return instance, False
        else:
            return self.init_instance(row), True

    def init_instance(self, row=None):
        if not row:
            row = {}
        instance = QualityTest()
        for attr, value in row.items():
            setattr(instance, attr, value)
        if FluorescenceQuantification.objects.all().count() == 0:
            instance.id = "1"
        else:
            instance.id = str(
                int(FluorescenceQuantification.objects.latest('id').id) + 1)
        instance.fq_number = row['实验编号']
        instance.test_number = row['试剂批号']
        instance.bis_begin = row['BIS起始量(ng)']
        instance.bis_template = row['BIS模板量(ul)']
        instance.bis_elution = row['BIS洗脱体积(ul)']
        instance.is_quality = row['有无质控']
        instance.operator = BmsUser.objects.get(username=row['操作人员'])
        instance.bs_date = row['BS实验日期']
        instance.note = row["实验异常备注"]
        instance.save()
        return instance


class FluorescenceQuantificationAdmin(ImportExportActionModelAdmin):
    """荧光定量管理"""
    list_per_page = 50
    search_fields = ("status", "fq_date")
    save_on_top = False
    list_display = (
        'fq_number', "boxes", 'test_number', 'operator', 'fq_date', "status",
    )
    list_display_links = ('fq_number',)
    form = FluorescenceQuantificationForm

    fieldsets = (
        ('实验相关信息', {
            'fields': ('boxes', "operator", "fq_date")
        }),
        ('实验数据', {
            'fields': ("test_number", ("instrument", 'loop_number'),
                       ("background", "is_quality"))
        }),
        ('内参ACTB', {
            'fields': (('actb_noise', "actb_ct", "actb_amp"),)
        }),
        ('SFRP2', {
            'fields': (('sfrp2_noise', "sfrp2_ct", "sfrp2_amp"),)
        }),
        ('SDC2', {
            'fields': (('sdc2_noise', "sdc2_ct", "sdc2_amp"),)
        }),
        ('实验结果', {
            'fields': ("result", 'note')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.status == 1 or obj.status == 2:
                self.readonly_fields = ['boxes', "operator", "fq_date",
                                        "test_number", "instrument",
                                        "background", "is_quality", "sfrp2_ct",
                                        "actb_ct", 'actb_noise', 'sfrp2_noise',
                                        "sfrp2_amp", "actb_amp", 'sdc2_noise',
                                        "sdc2_ct", "sdc2_amp", 'note',
                                        'loop_number']
                return self.readonly_fields
        except AttributeError:
            self.readonly_fields = []
            return self.readonly_fields
        self.readonly_fields = []
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.status == 1:
            ResultJudgement.objects.create(boxes=obj.boxes, fq=obj)
        else:
            pass
        obj.save()


class ResultJudgementAdmin(admin.ModelAdmin):
    list_per_page = 50
    search_fields = ["boxes", ]
    save_on_top = False
    list_display = (
        "boxes", 'fq_date', 'fq_operator'
    )
    list_display_links = ('boxes',)
    readonly_fields = ["boxes", "fq_date", "fq_operator", "fq_instrument",
                       "fq_actb_ct", "fq_actb_amp", "fq_sfrp2_ct",
                       "fq_sfrp2_amp", "fq_sdc2_ct", "fq_sdc2_amp",
                       "fq_is_qualified", ]

    def fq_date(self, obj):
        if obj.fq.fq_date:
            return obj.fq.fq_date
        else:
            return "-"

    def fq_operator(self, obj):
        if obj.fq.operator:
            return obj.fq.operator
        else:
            return "-"

    def fq_instrument(self, obj):
        if obj.fq.instrument:
            return obj.fq.instrument
        else:
            return "-"

    def fq_actb_ct(self, obj):
        if obj.fq.actb_ct:
            return obj.fq.actb_ct
        else:
            return "-"

    def fq_actb_amp(self, obj):
        if obj.fq.actb_amp:
            return obj.fq.actb_amp
        else:
            return "-"

    def fq_sfrp2_ct(self, obj):
        if obj.fq.sfrp2_ct:
            return obj.fq.sfrp2_ct
        else:
            return "-"

    def fq_sfrp2_amp(self, obj):
        if obj.fq.sfrp2_amp:
            return obj.fq.sfrp2_amp
        else:
            return "-"

    def fq_sdc2_ct(self, obj):
        if obj.fq.sdc2_ct:
            return obj.fq.sdc2_ct
        else:
            return "-"

    def fq_sdc2_amp(self, obj):
        if obj.fq.sdc2_amp:
            return obj.fq.sdc2_amp
        else:
            return "-"

    def fq_is_qualified(self, obj):
        if obj.fq.is_qualified:
            return obj.fq.is_qualified
        else:
            return "-"
