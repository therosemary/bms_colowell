from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin
from experiment.models import *
from django import forms


class ExtExecuteForm(forms.ModelForm):
    """提取任务表的字段限制"""

    class Meta:
        model = ExtExecute
        fields = "__all__"

    def clean_fail(self):
        sub = self.cleaned_data['submit']
        fa = self.cleaned_data["fail"]
        if sub and fa:
            raise forms.ValidationError(
                "请不要同时勾选任务完成和任务重做", code='invalid value'
            )
        else:
            return self.cleaned_data['fail']


class QualityTestForm(forms.ModelForm):
    """提取任务表的字段限制"""

    class Meta:
        model = QualityTest
        fields = "__all__"

    def clean_fail(self):
        sub = self.cleaned_data['submit']
        fa = self.cleaned_data["fail"]
        if sub and fa:
            raise forms.ValidationError(
                "请不要同时勾选任务完成和任务重做", code='invalid value'
            )
        else:
            return self.cleaned_data['fail']


class BsTaskForm(forms.ModelForm):
    """提取任务表的字段限制"""

    class Meta:
        model = BsTask
        fields = "__all__"

    def clean_fail(self):
        sub = self.cleaned_data['submit']
        fa = self.cleaned_data["fail"]
        if sub and fa:
            raise forms.ValidationError(
                "请不要同时勾选任务完成和任务重做", code='invalid value'
            )
        else:
            return self.cleaned_data['fail']


class FluorescenceQuantificationForm(forms.ModelForm):
    """提取任务表的字段限制"""

    class Meta:
        model = FluorescenceQuantification
        fields = "__all__"

    def clean_fail(self):
        sub = self.cleaned_data['submit']
        fa = self.cleaned_data["fail"]
        if sub and fa:
            raise forms.ValidationError(
                "请不要同时勾选任务完成和任务重做", code='invalid value'
            )
        else:
            return self.cleaned_data['fail']


class ExtExecuteAdmin(ImportExportActionModelAdmin):
    """提取管理"""
    form = ExtExecuteForm
    list_per_page = 50
    search_fields = ("status", "ext_date")
    save_on_top = False
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
                       ("elution_volume", "produce"))
        }),
        ('实验结果', {
            'fields': ('note', ("submit", "fail"))
        }),
    )

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
        except:
            return self.readonly_fields
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.submit:
            obj.status = 1
            obj.save()
        elif obj.fail:
            obj.status = 2
            obj.save()
        else:
            obj.save()


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
        except:
            return self.readonly_fields
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.submit:
            obj.status = 1
            obj.save()
        elif obj.fail:
            obj.status = 2
            obj.save()
        else:
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
        except:
            return self.readonly_fields
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.submit:
            obj.status = 1
            obj.save()
        elif obj.fail:
            obj.status = 2
            obj.save()
        else:
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
        except:
            return self.readonly_fields
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.submit:
            obj.status = 1
            obj.save()
        elif obj.fail:
            obj.status = 2
            obj.save()
        else:
            obj.save()
