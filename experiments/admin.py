from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from accounts.models import WechatInfo, BmsUser
from experiments.models import ResultJudgement
from experiments.resources import ExperimentsResource
from rangefilter.filter import DateRangeFilter
from bms_colowell.mixins import NotificationMixin
from bms_colowell.settings import DINGTALK_APPKEY, DINGTALK_SECRET, \
    DINGTALK_AGENT_ID, MEDIA_ROOT
from suggestions.models import Collections

info_middle = WechatInfo.objects.filter(bms_user=BmsUser.objects.filter
                                        (username="宋元元").first()).first()
EXPERIMENT_MIDDLE = info_middle.openid if info_middle else None
info_result1 = WechatInfo.objects.filter(bms_user=BmsUser.objects.filter
                                         (username="王美丛").first()).first()
info_result2 = WechatInfo.objects.filter(bms_user=BmsUser.objects.filter
                                         (username="王云霞").first()).first()
if info_result2 and info_result1:
    EXPERIMENT_RESULT = [info_result2.openid, info_result1.openid]
else:
    EXPERIMENT_RESULT = None


class ExperimentsAdmin(ImportExportActionModelAdmin, NotificationMixin):
    list_display = ("index_number", "receive_date", "ext_method", "submit_ext",
                    "submit_qua", "submit_bis", "submit_fq")
    list_display_links = ("index_number", "ext_method")
    resource_class = ExperimentsResource
    appkey = DINGTALK_APPKEY
    appsecret = DINGTALK_SECRET
    search_fields = ["index_number", "barcode"]
    fieldsets = (
        ('实验相关信息', {
            'fields': (
                'index_number', 'boxes', "receive_date",
                "projects_source")
        }),
        ('提取', {
            'fields': (
                ('ext_objective', "ext_method"),
                ("ext_start_number", "ext_hemoglobin"),
                ("ext_cz_volume", 'ext_density',),
                ("ext_elution_volume", 'produce_', "ext_qualified"),
                ("ext_operator", 'ext_date',), "ext_note",
                "submit_ext")
        }),
        ('质检', {
            'fields': (
                ('qua_test_number', "qua_instrument"),
                ("qua_sample_size", "qua_loop_number"),
                ("qua_background",),
                ("qua_noise", 'qua_ct', "qua_amplification_curve"),
                ("qua_is_quality",), ("qua_operator", "qua_date"),
                "qua_note", "submit_qua")
        }),
        ('BIS', {
            'fields': (
                ('bis_test_number', "bis_begin"),
                ("bis_template", "bis_elution"),
                ("bis_is_quality",),
                ("bis_date", 'bis_note'), "submit_bis")
        }),
        ('荧光定量', {
            'fields': (
                ('fq_test_number', "fq_instrument"),
                ("fq_loop_number",),
                ('fq_actb_ct', "fq_actb_amp"),
                ('fq_sfrp2_ct', "fq_sfrp2_amp"),
                ('fq_sdc2_ct', "fq_sdc2_amp"),
                ("fq_is_quality",), ("fq_operator", "fq_date"),
                "qualified_", "fq_suggest", "submit_fq")
        }),
        # (
        #         ('fq_test_number', "fq_instrument"),
        #         ("fq_loop_number", "fq_background"),
        #         ("fq_actb_noise", 'fq_actb_ct', "fq_actb_amp"),
        #         ("fq_sfrp2_noise", 'fq_sfrp2_ct', "fq_sfrp2_amp"),
        #         ("fq_sdc2_noise", 'fq_sdc2_ct', "fq_sdc2_amp"),
        #         ("fq_is_quality",), ("fq_operator", "fq_date"),
        #         "qualified_", "fq_suggest", "submit_fq")
        # }),
    )
    # readonly_fields = ["produce_", "qualified_", "ext_qualified"]
    actions = ["to_submit_ext", "to_submit_qua", "to_submit_bis",
               "to_submit_fq", "enter_result"]

    def enter_result(self, request, queryset):
        i = 0
        j = 0
        for obj in queryset:
            ResultJudgement.objects.create(experiment=obj)
            # TODO 调查问卷绑定外键
            # collection = Collections.objects.get()
            j += 1
        content = "{0}个任务成功进入结果判定".format(j)
        self.send_work_notice(content, DINGTALK_AGENT_ID, EXPERIMENT_RESULT)
        call_back = self.send_dingtalk_result
        message = "已钉钉通知" if call_back else "钉钉通知失败"
        self.message_user(request, message)

    enter_result.short_description = '进入结果判定'

    def to_submit_ext(self, request, queryset):
        i = 0
        j = 0
        for obj in queryset:
            if not obj.submit_ext:
                if obj.ext_hemoglobin:
                    obj.submit_ext = True
                    j += 1
                else:
                    pass
            else:
                i += 1
        content = "此次提交成功{0}个提取任务，{1}个任务已提交，请勿重复提交". \
            format(j, i)
        self.send_work_notice(content, DINGTALK_AGENT_ID, EXPERIMENT_MIDDLE)
        call_back = self.send_dingtalk_result
        message = "已钉钉通知" if call_back else "钉钉通知失败"
        self.message_user(request, message)

    to_submit_ext.short_description = '提交提取任务'

    def to_submit_qua(self, request, queryset):
        i = 0
        j = 0
        for obj in queryset:
            if not obj.submit_qua:
                if obj.qua_test_number and obj.qua_instrument:
                    obj.submit_qua = True
                    j += 1
                else:
                    pass
            else:
                i += 1
        content = "此次提交成功{0}个质检任务，{1}个任务已提交，请勿重复提交". \
            format(j, i)
        self.send_work_notice(content, DINGTALK_AGENT_ID, EXPERIMENT_MIDDLE)
        call_back = self.send_dingtalk_result
        message = "已钉钉通知" if call_back else "钉钉通知失败"
        self.message_user(request, message)

    to_submit_qua.short_description = '提交质检任务'

    def to_submit_bis(self, request, queryset):
        i = 0
        j = 0
        for obj in queryset:
            if not obj.submit_bis:
                if obj.bis_test_number and obj.bis_begin:
                    obj.submit_bis = True
                    j += 1
                else:
                    pass
            else:
                i += 1
        content = "此次提交成功{0}个BIS任务，{1}个任务已提交，请勿重复提交". \
            format(j, i)
        self.send_work_notice(content, DINGTALK_AGENT_ID, EXPERIMENT_MIDDLE)
        call_back = self.send_dingtalk_result
        message = "已钉钉通知" if call_back else "钉钉通知失败"
        self.message_user(request, message)

    to_submit_bis.short_description = '提交BIS任务'

    def to_submit_fq(self, request, queryset):
        i = 0
        j = 0
        for obj in queryset:
            if not obj.submit_fq:
                if obj.fq_test_number and obj.fq_instrument:
                    obj.submit_fq = True
                    j += 1
                else:
                    pass
            else:
                i += 1
        content = "此次提交成功{0}个荧光定量任务，{1}个任务已提交，请勿重复提交". \
            format(j, i)
        self.send_work_notice(content, DINGTALK_AGENT_ID, EXPERIMENT_MIDDLE)
        call_back = self.send_dingtalk_result
        message = "已钉钉通知" if call_back else "钉钉通知失败"
        self.message_user(request, message)

    to_submit_fq.short_description = '提交荧光定量任务'

    def get_list_filter(self, request):
        return ['submit_ext', "submit_qua", "submit_bis", "submit_fq",
                ('receive_date', DateRangeFilter)]

    def produce_(self, obj):
        if obj:
            if obj.elution_volume and obj.ext_density:
                pro = float(obj.elution_volume) * float(obj.ext_density)
                return pro
            else:
                return None
        return None

    produce_.short_description = "提取-产出"

    def qualified_(self, obj):
        if obj:
            try:
                if float(obj.fq_actb_ct) <= 38.5:
                    return "合格"
                else:
                    return "不合格"
            except TypeError:
                return None
        return None

    produce_.short_description = "荧光定量-是否合格"

    def ext_qualified(self, obj):
        if obj:
            if obj.elution_volume and obj.ext_density:
                pro = float(obj.elution_volume) * float(obj.ext_density)
                if pro > 2:
                    return "是"
                else:
                    return "否"
            else:
                return None
        return None

    ext_qualified.short_description = "提取-是否合格"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            readonly = ["produce_", "qualified_", "ext_qualified"]
            ext = ['ext_objective', "ext_method",
                   "ext_start_number", "ext_hemoglobin",
                   "ext_cz_volume", 'ext_density',
                   "ext_elution_volume", 'produce_', "ext_qualified",
                   "ext_operator", 'ext_date', "ext_note", "submit_ext"]
            qua = ['qua_test_number', "qua_instrument",
                   "qua_sample_size", "qua_loop_number",
                   "qua_background",
                   "qua_noise", 'qua_ct', "qua_amplification_curve",
                   "qua_is_quality", "qua_operator", "qua_date",
                   "qua_note", "submit_qua"]
            bis = ['bis_test_number', "bis_begin",
                   "bis_template", "bis_elution",
                   "bis_is_quality",
                   "bis_date", 'bis_note', "submit_bis"]
            fq = ['fq_test_number', "fq_instrument",
                  "fq_loop_number", "fq_background",
                  "fq_actb_noise", 'fq_actb_ct', "fq_actb_amp",
                  "fq_sfrp2_noise", 'fq_sfrp2_ct', "fq_sfrp2_amp",
                  "fq_sdc2_noise", 'fq_sdc2_ct', "fq_sdc2_amp",
                  "fq_is_quality", "fq_operator", "fq_date",
                  "qualified_", "fq_suggest", "submit_fq"]
            if obj.submit_ext:
                readonly.extend(ext)
            if obj.submit_qua:
                readonly.extend(qua)
            if obj.submit_bis:
                readonly.extend(bis)
            if obj.submit_fq:
                readonly.extend(fq)
            return readonly
        else:
            return ["produce_", "qualified_", "ext_qualified"]

    # def get_actions(self, request):
    #     if request.user.has_perm("")


class ResultJudgementAdmin(admin.ModelAdmin):
    list_display = ["experiment", "risk", "SDC2", "SFRP2", "res_date",
                    "submit"]
    list_display_links = ["experiment", ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.submit:
                return ['fq_instrument', "fq_actb_ct", "fq_actb_amp",
                        "fq_sdc2_ct", "fq_sdc2_amp", "fq_sfrp2_ct",
                        'fq_sfrp2_amp', "qualified_", "experiment",
                        "collection", "experiment", "risk", "SDC2", "SFRP2",
                        "res_date", "submit", "risk_file", "ext_hemoglobin"]
            if request.user.has_perm("experiments.change_resultjudgement"):
                return ['fq_instrument', "fq_actb_ct", "fq_actb_amp",
                        "fq_sdc2_ct", "fq_sdc2_amp", "fq_sfrp2_ct",
                        'fq_sfrp2_amp', "qualified_", "experiment",
                        "collection", "ext_hemoglobin"]
            else:
                return ['fq_instrument', "fq_actb_ct", "fq_actb_amp",
                        "fq_sdc2_ct", "fq_sdc2_amp", "fq_sfrp2_ct",
                        'fq_sfrp2_amp', "qualified_", "experiment",
                        "collection", "ext_hemoglobin"]
        else:
            return ['fq_instrument', "fq_actb_ct", "fq_actb_amp", "fq_sdc2_ct",
                    "fq_sdc2_amp", "fq_sfrp2_ct", 'fq_sfrp2_amp', "qualified_",
                    "experiment", "collection", "ext_hemoglobin"]

    def get_fieldsets(self, request, obj=None):
        if request.user.has_perm("experiments.change_resultjudgement"):
            return (
                ('结果判定', {
                    'fields': ("experiment", 'ext_hemoglobin',
                               'fq_instrument', ("fq_actb_ct", "fq_actb_amp"),
                               ("fq_sdc2_ct", "fq_sdc2_amp"),
                               ("fq_sfrp2_ct", 'fq_sfrp2_amp',),
                               "qualified_", "risk", ('SDC2', "SFRP2"),
                               "res_date", "submit")
                }),
            )
        else:
            return (

                ('结果判定', {
                    'fields': ('ext_hemoglobin', "risk", ('SDC2', "SFRP2"),
                               "res_date", "risk_file", "submit")
                }),
            )

    def qualified_(self, obj):
        if obj:
            try:
                if float(obj.experiment.fq_actb_ct) <= 38.5:
                    return "合格"
                else:
                    return "不合格"
            except TypeError:
                return None
        return None

    qualified_.short_description = "QPCR是否合格"

    def fq_instrument(self, obj):
        if obj:
            return obj.experiment.fq_instrument
        else:
            return None

    fq_instrument.short_description = "荧光定量-仪器"

    def fq_actb_ct(self, obj):
        if obj:
            return obj.experiment.fq_actb_ct
        else:
            return None

    fq_actb_ct.short_description = "荧光定量-ACTB_CT值"

    def fq_actb_amp(self, obj):
        if obj:
            return obj.experiment.fq_actb_amp
        else:
            return None

    fq_actb_amp.short_description = "荧光定量-ACTB_扩增曲线"

    def fq_sfrp2_ct(self, obj):
        if obj:
            return obj.experiment.fq_sfrp2_ct
        else:
            return None

    fq_sfrp2_ct.short_description = "荧光定量-SFRP2_CT值"

    def fq_sfrp2_amp(self, obj):
        if obj:
            return obj.experiment.fq_sfrp2_amp
        else:
            return None

    fq_sfrp2_amp.short_description = "荧光定量-SFRP2_扩增曲线"

    def fq_sdc2_ct(self, obj):
        if obj:
            return obj.experiment.fq_sdc2_ct
        else:
            return None

    fq_sdc2_ct.short_description = "荧光定量-SDC2_CT值"

    def fq_sdc2_amp(self, obj):
        if obj:
            return obj.experiment.fq_sdc2_amp
        else:
            return None

    fq_sdc2_amp.short_description = "荧光定量-SDC2_C扩增曲线"

    def ext_hemoglobin(self, obj):
        if obj:
            return obj.experiment.ext_hemoglobin
        else:
            return None

    ext_hemoglobin.short_description = "血红蛋白"
