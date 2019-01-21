from import_export.admin import ImportExportActionModelAdmin
from experiment.forms import ExtExecuteForm, QualityTestForm, BsTaskForm, \
    FluorescenceQuantificationForm
from import_export import resources
from experiment.models import *
from accounts.models import *


class ExtExecuteResource(resources.ModelResource):
    class Meta:
        model = ExtExecute
        skip_unchanged = True
        import_id_fields = 'ext_number'
        fields = ('ext_number', 'operator',
                  'test_number', 'ext_method', "objective", 'start_number',
                  'hemoglobin', 'cizhutiji', 'ext_density','elution_volume',
                  "ext_date", "note")
        export_order =  ('ext_number', 'operator',
                  'test_number', 'ext_method', "objective", 'start_number',
                  'hemoglobin', 'cizhutiji', 'ext_density','elution_volume',
                  "ext_date", "note")

    def get_export_headers(self):
        return ["实验编号", "操作人员", "试剂批号", "提取方法", "目的",
                "起始取样量(ml)", "血红蛋白", "磁珠体积(ul)", "提取浓度(ng/ul)",
                "洗脱体积(ul)", "提取日期", "实验异常备注"]

    def get_diff_headers(self):
        return ["实验编号", "操作人员", "试剂批号", "提取方法", "目的",
                "起始取样量(ml)", "血红蛋白", "磁珠体积(ul)", "提取浓度(ng/ul)",
                "洗脱体积(ul)", "提取日期", "实验异常备注"]

    def get_or_init_instance(self, instance_loader, row):
        instance = self.get_instance(instance_loader, row)
        if instance:
            # instance.operator = BmsUser.objects.get()
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
            return (instance, False)
        else:
            return (self.init_instance(row), True)

    def init_instance(self, row=None):
        if not row:
            row = {}
        instance = self._meta.model()
        for attr, value in row.items():
            setattr(instance, attr, value)
        if ExtExecute.objects.all().count() == 0:
            instance.id = "1"
        else:
            instance.id = str(int(ExtExecute.objects.latest('id').id) + 1)
        return instance


class ExtExecuteAdmin(ImportExportActionModelAdmin):
    """提取管理"""
    form = ExtExecuteForm
    list_per_page = 50
    search_fields = ("status", "ext_date")
    save_on_top = False
    resource_class = ExtExecuteResource
    list_display = (
        'ext_number', "boxes", "test_number", 'ext_method', 'ext_date',
        'status',
    )
    list_display_links = ('ext_number',)
    fieldsets = (
        ('实验相关信息', {
            'fields': ('boxes', 'ext_method', 'ext_times', "operator",
                       "ext_date")
        }),
        ('实验数据', {
            'fields': ("test_number", ('start_number', "hemoglobin"),
                       ("cizhutiji", "ext_density"),
                       ("elution_volume", ))
        }),
        ('实验结果', {
            'fields': ('note', ("submit", "fail"))
        }),
    )

    # def produce(self):
    #     if

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.status == 1 or obj.status == 2:
                self.readonly_fields = ['boxes', 'ext_method', 'ext_times',
                                        "operator", "ext_date", "test_number",
                                        'start_number', "hemoglobin",
                                        "cizhutiji", "ext_density",
                                        "elution_volume", "produce", 'note',
                                        "submit", "fail"]
                return self.readonly_fields
        except AttributeError:
            self.readonly_fields = []
            return self.readonly_fields
        self.readonly_fields = []
        return self.readonly_fields

    # def save_model(self, request, obj, form, change):
    #     if obj.submit:
    #         QualityTest.objects.create(boxes=obj.boxes, qua_number= obj.)
    #     elif obj.fail:
    #         obj.status = 2
    #     obj.save()


class QualityTestAdmin(ImportExportActionModelAdmin):
    """质检管理"""
    list_per_page = 50
    search_fields = ("status", "qua_date")
    save_on_top = False
    list_display = (
        'qua_number', "boxes", 'test_number', 'operator', 'qua_date',
        "status",
    )
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
            'fields': ('note', ("submit", "fail"))
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.status == 1 or obj.status == 2:
                self.readonly_fields = ['boxes', "operator", "qua_date",
                                        "test_number", "instrument",
                                        'template_number', "loop_number",
                                        "background_baseline", "ct",
                                        "amplification_curve", "submit",
                                        'note', "threshold_line", "fail"]
                return self.readonly_fields
        except AttributeError:
            self.readonly_fields = []
            return self.readonly_fields
        self.readonly_fields = []
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.submit:
            obj.status = 1
        elif obj.fail:
            obj.status = 2
        obj.save()


class BsTaskAdmin(ImportExportActionModelAdmin):
    """BS管理"""
    list_per_page = 50
    search_fields = ("status", "bs_date")
    save_on_top = False
    list_display = (
        'bs_number', "boxes", 'test_number', "bs_times", 'operator', 'bs_date',
        "status",
    )
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
            'fields': ('note', ("submit", "fail"))
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.status == 1 or obj.status == 2:
                self.readonly_fields = ['boxes', "operator", "bs_times",
                                        "bs_date", "test_number", "bis_begin",
                                        'bis_template', "bis_elution", 'note',
                                        "is_quality", "submit", "fail"]
                return self.readonly_fields
        except AttributeError:
            self.readonly_fields = []
            return self.readonly_fields
        self.readonly_fields = []
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.submit:
            obj.status = 1
        elif obj.fail:
            obj.status = 2
        obj.save()


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
            'fields': ("result", 'note', ("submit", "fail"))
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.status == 1 or obj.status == 2:
                self.readonly_fields = ['boxes', "operator", "fq_date",
                                        "test_number", "instrument", "fail",
                                        "background", "is_quality", "sfrp2_ct",
                                        "actb_ct", 'actb_noise', 'sfrp2_noise',
                                        "sfrp2_amp", "actb_amp", 'sdc2_noise',
                                        "sdc2_ct", "sdc2_amp", 'note',
                                        "submit", 'loop_number']
                return self.readonly_fields
        except AttributeError:
            self.readonly_fields = []
            return self.readonly_fields
        self.readonly_fields = []
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.submit:
            obj.status = 1
        elif obj.fail:
            obj.status = 2
        obj.save()
