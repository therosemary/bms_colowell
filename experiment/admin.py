from django.contrib.auth.models import Group
from django.db.models import Q
from import_export.admin import ImportExportActionModelAdmin
from tech_support.models import Techsupport
from django.contrib import admin
from accounts.models import BmsUser
from experiment.forms import ExtExecuteForm, QualityTestForm, BsTaskForm, \
    FluorescenceQuantificationForm
from import_export import resources
from experiment.models import *
from experiment.resources import ExtExecuteResource, QualityTestResource, \
    BsTaskResource, FluorescenceQuantificationResource

Monthchoose = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G",
               8: "H", 9: "I", 10: "G", 11: "K", 12: "L", }


@admin.register(ExtExecute)
class ExtExecuteAdmin(ImportExportActionModelAdmin):
    """提取管理"""
    form = ExtExecuteForm
    list_per_page = 50
    search_fields = ('ext_number', "boxes",)
    save_on_top = False
    resource_class = ExtExecuteResource
    list_display = (
        'ext_number', "boxes", "ext_times", "test_number", 'ext_method',
        'ext_date', 'status',
    )
    readonly_fields = ["produce_", "is_qualified", "ext_times", 'hemoglobin',
                       'ext_method', "operator", "test_number", 'start_number',
                       "boxes", "cizhutiji", "ext_density", "elution_volume",
                       'note']
    list_display_links = ('ext_number',)
    autocomplete_fields = ("boxes",)
    fieldsets = (
        ('实验相关信息', {
            'fields': ('boxes', "ext_times", 'ext_method', "operator",
                       "ext_date")
        }),
        ('实验数据', {
            'fields': ("test_number", ('start_number', "hemoglobin"),
                       ("cizhutiji", "ext_density"),
                       ("elution_volume", 'produce_',), "is_qualified")
        }),
        ('实验结果', {
            'fields': ('note', "submit")
        }),
    )
    actions = ["a1", "a2"]

    def a1(self, request, queryset):
        q = 0
        n = 0
        for i in queryset:
            if not i.status:
                i.status = 0
                i.save()
                n += 1
            else:
                q += 1
        self.message_user(
            request, "已成功提交{0}个盒子样本至实验总监,{1}个盒子提交失败".
                format(n, q))

    a1.short_description = '提交至实验总监'

    def a2(self, request, queryset):
        n = 0
        for i in queryset:
            n += 1
        self.message_user(request, "已成功提交{0}个盒子样本".format(n))

    a2.short_description = '提交所选抽提任务'

    def get_actions(self, request):
        actions = super().get_actions(request)
        try:
            current_group_set = Group.objects.filter(user=request.user)
            if len(current_group_set) == 1:
                if current_group_set[0].name == "实验部":
                    del actions['a2']
                    return actions
                elif current_group_set[0].name == "实验总监":
                    del actions['a1']
                    return actions
                else:
                    return actions
            else:
                names = [i.name for i in current_group_set]
                if "实验部" in names:
                    del actions['a2']
                    return actions
                elif "实验总监" in names:
                    del actions['a1']
                    return actions
                else:
                    return actions
        except AttributeError:
            pass
        return actions

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        try:
            current_group_set = Group.objects.filter(user=request.user)
            if len(current_group_set) == 1:
                if current_group_set[0].name == "实验部":
                    return qs
                elif current_group_set[0].name == "实验总监":
                    print(qs)
                    return qs.filter(
                        Q(status=0) | Q(status=1) | Q(status=2)
                        | Q(status=3) | Q(status=4))
                else:
                    return qs
            else:
                names = [i.name for i in current_group_set]
                if "实验部" in names:
                    return qs
                elif "实验总监" in names:
                    return qs.filter(
                        Q(status=0) | Q(status=1) | Q(status=2)
                        | Q(status=3) | Q(status=4))
        except AttributeError:
            pass
        return qs

    def get_fieldsets(self, request, obj=None):
        current_group_set = Group.objects.filter(user=request.user)
        for i in current_group_set:
            if i.name == "实验部":
                return self.fieldsets
            elif i.name == "实验总监":
                return (
                    ('实验相关信息', {
                        'fields': (
                            'boxes', 'ext_method', "operator",
                            "ext_date", "ext_times")
                    }),
                    ('实验数据', {
                        'fields': (
                            "test_number", ('start_number', "hemoglobin"),
                            ("cizhutiji", "ext_density"),
                            ("elution_volume", 'produce_',), "is_qualified")
                    }),
                    ('实验结果', {
                        'fields': ("status", 'note', "submit")
                    }),
                )
        return self.fieldsets

    def produce_(self, obj):
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
            if obj.submit:
                return ['boxes', 'ext_method',
                        "operator", "ext_date", "test_number",
                        'start_number', "hemoglobin",
                        "cizhutiji", "ext_density", "submit",
                        "elution_volume", "produce_",
                        "is_qualified", 'note', "ext_times", "status"]
        except AttributeError:
            pass
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        # if form.cleaned_data["boxes"]:
        #     box = form.cleaned_data["boxes"]
        # else:
        box = obj.boxes
        query_ext = ExtExecute.objects.filter(boxes=box)
        if not obj.ext_number:
            # box = form.cleaned_data["boxes"]
            # query_ext = ExtExecute.objects.filter(boxes=box)
            # if query_ext.count() == 1:
            #     if "_" not in query_ext.first().ext_number:
            #         obj.ext_number = query_ext.first().ext_number + "_1"
            # elif query_ext.count() > 1:
            #     index = 0
            #     for i in query_ext:
            #         if "_" in i.ext_number:
            #             if index < int(i.ext_number[-1]):
            #                 index = int(i.ext_number[-1])
            #     obj.ext_number = query_ext.first().ext_number + "_" + str(
            #         index + 1)
            # else:
            #     obj.ext_number = "违规：该盒子技术支持尚未下单"
            box = form.cleaned_data["boxes"]
            obj.ext_number = query_ext.first().ext_number
        if change:
            if not obj.ext_times:
                obj.ext_times = query_ext.count()
                obj.save()
        else:
            if not obj.ext_times:
                obj.ext_times = query_ext.count() + 1
                obj.save()
        if obj.submit:

            query_qua = QualityTest.objects.filter(boxes=box)
            query_bs = BsTask.objects.filter(boxes=box)
            if obj.status == 1:
                ExtExecute.objects.create(boxes=box,
                                          ext_number=obj.ext_number,
                                          ext_times=obj.ext_times + 1)
                if box.status < 2:
                    box.status = 2
                    box.save()
            elif obj.status == 2:

                QualityTest.objects.create(qua_number=obj.ext_number,
                                           boxes=box,
                                           ext_times=obj.ext_times,
                                           qua_times=query_qua.count() + 1
                                           )
                if box.status < 4:
                    box.status = 4
                    box.save()
            elif obj.status == 3:

                BsTask.objects.create(bs_number=obj.ext_number,
                                      boxes=box,
                                      ext_times=obj.ext_times,
                                      qua_times=query_qua.count(),
                                      bs_times=query_bs.count() + 1
                                      )
                if box.status < 6:
                    box.status = 6
                    box.save()
            else:
                pass
        else:
            pass
        if box.status < 3:
            box.status = 3
            box.save()
        obj.save()


class QualityTestAdmin(ImportExportActionModelAdmin):
    """质检管理"""
    list_per_page = 50
    search_fields = ('qua_number', "status", "qua_date")
    save_on_top = False
    list_display = (
        'qua_number', "boxes", "ext_times", "qua_times", 'test_number',
        'operator', 'qua_date', "status",
    )
    autocomplete_fields = ("boxes",)
    resource_class = QualityTestResource
    readonly_fields = ['boxes', "operator", "qua_date",
                       "test_number", "instrument",
                       'template_number', "loop_number",
                       "background_baseline", "ct",
                       "amplification_curve",
                       'note', "noise", ]
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
            'fields': ("ct", "amplification_curve", "noise")
        }),
        ('实验结果', {
            'fields': ('note',)
        }),
    )
    actions = ["a1", "a2"]

    def a1(self, request, queryset):
        q = 0
        n = 0
        for i in queryset:
            if not i.status:
                i.status = 0
                i.save()
                n += 1
            else:
                q += 1
        self.message_user(
            request,
            "已成功提交{0}个盒子样本至实验总监,{1}个盒子提交失败".format(n, q)
        )

    a1.short_description = '提交至实验总监'

    def a2(self, request, queryset):
        n = 0
        for i in queryset:
            n += 1
        self.message_user(request, "已成功提交{0}个盒子样本".format(n))

    a2.short_description = '提交所选质检任务'

    def get_actions(self, request):
        actions = super().get_actions(request)
        try:
            current_group_set = Group.objects.filter(user=request.user)
            if len(current_group_set) == 1:
                if current_group_set[0].name == "实验部":
                    del actions['a2']
                    return actions
                elif current_group_set[0].name == "实验总监":
                    del actions['a1']
                    return actions
                else:
                    return actions
            else:
                names = [i.name for i in current_group_set]
                if "实验部" in names:
                    del actions['a2']
                    return actions
                elif "实验总监" in names:
                    del actions['a1']
                    return actions
                else:
                    return actions
        except AttributeError:
            pass
        return actions

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        try:
            current_group_set = Group.objects.filter(user=request.user)
            if len(current_group_set) == 1:
                if current_group_set[0].name == "实验部":
                    return qs
                elif current_group_set[0].name == "实验总监":
                    print(qs)
                    return qs.filter(
                        Q(status=0) | Q(status=1) | Q(status=2)
                        | Q(status=3) | Q(status=4))
                else:
                    return qs
            else:
                names = [i.name for i in current_group_set]
                if "实验部" in names:
                    return qs
                elif "实验总监" in names:
                    return qs.filter(
                        Q(status=0) | Q(status=1) | Q(status=2)
                        | Q(status=3) | Q(status=4))
        except AttributeError:
            pass
        return qs

    def get_fieldsets(self, request, obj=None):
        current_group_set = Group.objects.filter(user=request.user)
        for i in current_group_set:
            if i.name == "实验部":
                return self.fieldsets
            elif i.name == "实验总监":
                return (
                    ('实验相关信息', {
                        'fields': ('boxes', "operator", "qua_date")
                    }),
                    ('实验数据', {
                        'fields': (
                            "test_number", ("instrument", 'template_number'),
                            ("loop_number", "background_baseline"))
                    }),
                    ('非甲基化ACTB', {
                        'fields': (
                            "ct", "amplification_curve", "noise")
                    }),
                    ('实验结果', {
                        'fields': ("status", 'note', "submit")
                    }),
                )
        return self.fieldsets

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.submit:
                return ['boxes', "operator", "qua_date",
                        "test_number", "instrument",
                        'template_number', "loop_number",
                        "background_baseline", "ct",
                        "amplification_curve", "status",
                        'note', "noise", "submit"]
        except AttributeError:
            pass
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        # if form.cleaned_data["boxes"]:
        #     box = form.cleaned_data["boxes"]
        # else:
        box = obj.boxes
        query_ext = ExtExecute.objects.filter(boxes=box)
        query_qua = QualityTest.objects.filter(boxes=box)
        query_bs = BsTask.objects.filter(boxes=box)
        if not obj.qua_number:
            # box = form.cleaned_data["boxes"]
            # query_ = ExtExecute.objects.filter(boxes=box)
            # if query_.count() == 1:
            #     index_ = query_.first().ext_number
            #     qua = QualityTest.objects.get(qua_number=index_)
            #     if qua:
            #         obj.qua_number = "编号：{}的提取实验已有质检记录,请核对". \
            #             format(index_)
            #     else:
            #         obj.qua_number = index_
            # elif query_.count() > 1:
            #     index_loop = 0
            # if "_" not in query_.first():
            #     a = query_.first().qua_number
            # else:
            #     a = query_.first().qua_number.split("_")[0]
            #     qua_ = None
            #     for i in query_:
            #         if "_" in i.qua_number:
            #             if index_loop < int(i.qua_number[-1]):
            #                 index_loop = int(i.qua_number[-1])
            #                 qua_ = i
            #     if qua_:
            #         obj.qua_number = qua_.ext_number
            #     else:
            #         obj.qua_number = "未查到带有_的实验号，请核实"
            # else:
            #     qr = ExtExecute.objects.filter(boxes=box)
            #     if qr.count() == 0:
            #         err = "该样本还未经过提取，请核对"
            #         obj.bs_number = err
            #     else:
            #         for i in qr:
            #             if "_" not in i.ext_number:
            #                 number = i.ext_number
            #                 obj.qua_number = number
            # if not obj.bs_number:
            #     obj.bs_number = "未找到该样本"
            # obj.bs_number = ""
            obj.ext_times = query_ext.count()
            obj.qua_times = query_qua.count() + 1
            obj.qua_number = query_ext.first().qua_number
        if obj.submit:
            if obj.status == 1:
                ExtExecute.objects.create(boxes=box,
                                          ext_number=
                                          query_qua.first().ext_number,
                                          ext_times=query_ext.count() + 1)
                if box.status < 2:
                    box.status = 2
                    box.save()
            elif obj.status == 2:
                QualityTest.objects.create(qua_number=obj.qua_number,
                                           boxes=box,
                                           ext_times=obj.ext_times,
                                           qua_times=query_qua.count() + 1
                                           )
                if box.status < 4:
                    box.status = 4
                    box.save()
            elif obj.status == 3:
                BsTask.objects.create(bs_number=obj.qua_number,
                                      boxes=box,
                                      ext_times=obj.ext_times,
                                      qua_times=query_qua.count(),
                                      bs_times=query_bs.count() + 1
                                      )
                if box.status < 6:
                    box.status = 4
                    box.save()
            else:
                pass
        else:
            pass
        if box.status < 5:
            box.status = 5
            box.save()
        obj.save()


class BsTaskAdmin(ImportExportActionModelAdmin):
    """BS管理"""
    list_per_page = 50
    search_fields = ("status", "bs_date")
    save_on_top = False
    list_display = (
        'bs_number', "boxes", "ext_times", "qua_times", "bs_times",
        'test_number', 'operator', 'bs_date', "status",
    )
    resource_class = BsTaskResource
    list_display_links = ('bs_number',)
    autocomplete_fields = ("boxes",)
    form = BsTaskForm
    fieldsets = (
        ('实验相关信息', {
            'fields': ('bs_number', 'boxes', "operator", "bs_times", "bs_date")
        }),
        ('实验数据', {
            'fields': ("test_number", ("bis_begin", 'bis_template'),
                       ("bis_elution", "is_quality"))
        }),
        ('实验结果', {
            'fields': ('note',)
        }),
    )
    actions = ["a1", "a2"]

    def a1(self, request, queryset):
        q = 0
        n = 0
        for i in queryset:
            if not i.status:
                i.status = 0
                i.save()
                n += 1
            else:
                q += 1
        self.message_user(
            request,
            "已成功提交{0}个盒子样本至实验总监,{1}个盒子提交失败".format(n, q)
        )

    a1.short_description = '提交至实验总监'

    def a2(self, request, queryset):
        n = 0
        for i in queryset:
            n += 1
        self.message_user(request, "已成功提交{0}个盒子样本".format(n))

    a2.short_description = '提交所选BS任务'

    def get_actions(self, request):
        actions = super().get_actions(request)
        try:
            current_group_set = Group.objects.filter(user=request.user)
            if len(current_group_set) == 1:
                if current_group_set[0].name == "实验部":
                    del actions['a2']
                    return actions
                elif current_group_set[0].name == "实验总监":
                    del actions['a1']
                    return actions
                else:
                    return actions
            else:
                names = [i.name for i in current_group_set]
                if "实验部" in names:
                    del actions['a2']
                    return actions
                elif "实验总监" in names:
                    del actions['a1']
                    return actions
                else:
                    return actions
        except AttributeError:
            pass
        return actions

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        try:
            current_group_set = Group.objects.filter(user=request.user)
            if len(current_group_set) == 1:
                if current_group_set[0].name == "实验部":
                    return qs
                elif current_group_set[0].name == "实验总监":
                    print(qs)
                    return qs.filter(
                        Q(status=0) | Q(status=1) | Q(status=2)
                        | Q(status=3) | Q(status=4))
                else:
                    return qs
            else:
                names = [i.name for i in current_group_set]
                if "实验部" in names:
                    return qs
                elif "实验总监" in names:
                    return qs.filter(
                        Q(status=0) | Q(status=1) | Q(status=2)
                        | Q(status=3) | Q(status=4))
        except AttributeError:
            pass
        return qs

    def get_fieldsets(self, request, obj=None):
        current_group_set = Group.objects.filter(user=request.user)
        for i in current_group_set:
            if i.name == "实验部":
                return self.fieldsets
            elif i.name == "实验总监":
                return (
                    ('实验相关信息', {
                        'fields': ('bs_number', 'boxes', "operator",
                                   "bs_times", "bs_date")
                    }),
                    ('实验数据', {
                        'fields': (
                            "test_number", ("bis_begin", 'bis_template'),
                            ("bis_elution", "is_quality"))
                    }),
                    ('实验结果', {
                        'fields': ("status", 'note', "submit")
                    }),
                )
        return self.fieldsets

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.submit:
                return ['boxes', "operator", "bs_times", "status",
                        "bs_date", "test_number", "bis_begin",
                        'bis_template', "bis_elution", 'note', 'bs_number',
                        "is_quality", "ext_times", "qua_times", "submit"]
        except AttributeError:
            pass
        return ['boxes', "operator", "bs_times", "bs_date", "test_number",
                "bis_begin", 'bis_template', "bis_elution", 'note',
                'bs_number', "is_quality", "ext_times", "qua_times"]

    def save_model(self, request, obj, form, change):
        # if form.cleaned_data["boxes"]:
        #     box = form.cleaned_data["boxes"]
        # else:
        box = obj.boxes
        query_ext = ExtExecute.objects.filter(boxes=box)
        query_qua = QualityTest.objects.filter(boxes=box)
        query_bs = BsTask.objects.filter(boxes=box)
        query_flu = FluorescenceQuantification.objects.filter(boxes=box)
        if not obj.bs_number:
            obj.ext_times = query_ext.count()
            obj.qua_times = query_qua.count()
            obj.bs_times = query_bs.count()
            obj.bs_number = query_ext.first().qua_number
        if obj.submit:
            if obj.status == 1:
                ExtExecute.objects.create(boxes=box,
                                          ext_number=
                                          query_qua.first().ext_number,
                                          ext_times=query_ext.count() + 1)
                if box.status < 2:
                    box.status = 2
                    box.save()
            elif obj.status == 2:
                BsTask.objects.create(bs_number=obj.bs_number,
                                      boxes=box,
                                      ext_times=obj.ext_times,
                                      qua_times=obj.qua_times,
                                      bs_times=query_bs.count() + 1)
                if box.status < 6:
                    box.status = 6
                    box.save()
            elif obj.status == 3:
                FluorescenceQuantification.objects.create(
                    fq_number=obj.bs_number,
                    boxes=box,
                    ext_times=obj.ext_times,
                    qua_times=obj.qua_times,
                    bs_times=obj.bs_times,
                    flu_times=query_flu.count() + 1)
                if box.status < 8:
                    box.status = 8
                    box.save()
            else:
                pass
        else:
            pass
        if box.status < 7:
            box.status = 7
            box.save()
        obj.save()


class FluorescenceQuantificationAdmin(ImportExportActionModelAdmin):
    """荧光定量管理"""
    list_per_page = 50
    search_fields = ("status", "fq_date")
    save_on_top = False
    list_display = (
        'fq_number', "boxes", "ext_times", "qua_times",
        "bs_times", "flu_times", 'test_number', 'operator', 'fq_date', "status"
    )
    list_display_links = ('fq_number',)
    form = FluorescenceQuantificationForm
    autocomplete_fields = ("boxes",)
    resource_class = FluorescenceQuantificationResource
    fieldsets = (
        ('实验相关信息', {
            'fields': ('fq_number', 'boxes', "ext_times", "qua_times",
                       "bs_times", "flu_times", "operator", "fq_date")
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
    actions = ["a1", "a2"]

    def a1(self, request, queryset):
        q = 0
        n = 0
        for i in queryset:
            if not i.status:
                i.status = 0
                i.save()
                n += 1
            else:
                q += 1
        self.message_user(
            request,
            "已成功提交{0}个盒子样本至实验总监,{1}个盒子提交失败".format(n, q)
        )

    a1.short_description = '提交至实验总监'

    def a2(self, request, queryset):
        n = 0
        for i in queryset:
            n += 1
        self.message_user(request, "已成功提交{0}个盒子样本".format(n))

    a2.short_description = '提交所选BS任务'

    def get_actions(self, request):
        actions = super().get_actions(request)
        try:
            current_group_set = Group.objects.filter(user=request.user)
            if len(current_group_set) == 1:
                if current_group_set[0].name == "实验部":
                    del actions['a2']
                    return actions
                elif current_group_set[0].name == "实验总监":
                    del actions['a1']
                    return actions
                else:
                    return actions
            else:
                names = [i.name for i in current_group_set]
                if "实验部" in names:
                    del actions['a2']
                    return actions
                elif "实验总监" in names:
                    del actions['a1']
                    return actions
                else:
                    return actions
        except AttributeError:
            pass
        return actions

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        try:
            current_group_set = Group.objects.filter(user=request.user)
            if len(current_group_set) == 1:
                if current_group_set[0].name == "实验部":
                    return qs
                elif current_group_set[0].name == "实验总监":
                    print(qs)
                    return qs.filter(
                        Q(status=0) | Q(status=1) | Q(status=2)
                        | Q(status=3) | Q(status=4))
                else:
                    return qs
            else:
                names = [i.name for i in current_group_set]
                if "实验部" in names:
                    return qs
                elif "实验总监" in names:
                    return qs.filter(
                        Q(status=0) | Q(status=1) | Q(status=2)
                        | Q(status=3) | Q(status=4))
        except AttributeError:
            pass
        return qs

    def get_fieldsets(self, request, obj=None):
        current_group_set = Group.objects.filter(user=request.user)
        for i in current_group_set:
            if i.name == "实验部":
                return self.fieldsets
            elif i.name == "实验总监":
                return (
                    ('实验相关信息', {
                        'fields': ('fq_number', 'boxes', "ext_times",
                                   "qua_times", "bs_times", "flu_times",
                                   "operator", "fq_date")
                    }),
                    ('实验数据', {
                        'fields': ("test_number",
                                   ("instrument", 'loop_number'),
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
                        'fields': ("result", "status", 'note', "submit")
                    }),
                )
        return self.fieldsets

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.submit:
                return ['boxes', "operator", "fq_date",
                        "test_number", "instrument", "fq_number", "result",
                        "background", "is_quality", "sfrp2_ct", "status",
                        "actb_ct", 'actb_noise', 'sfrp2_noise',
                        "sfrp2_amp", "actb_amp", 'sdc2_noise',
                        "sdc2_ct", "sdc2_amp", 'note', "submit",
                        'loop_number', "ext_times", "qua_times",
                        "bs_times", "flu_times"]
        except AttributeError:
            pass
        return ['boxes', "operator", "fq_date",
                "test_number", "instrument", "fq_number", "result",
                "background", "is_quality", "sfrp2_ct",
                "actb_ct", 'actb_noise', 'sfrp2_noise',
                "sfrp2_amp", "actb_amp", 'sdc2_noise',
                "sdc2_ct", "sdc2_amp", 'note',
                'loop_number', "ext_times", "qua_times",
                "bs_times", "flu_times"]

    # 旧的命名规则
    # def save_model(self, request, obj, form, change):
    #     if not obj.fq_number:
    #         box = form.cleaned_data["boxes"]
    #         query_ = FluorescenceQuantification.objects.filter(boxes=box)
    #         if query_.count() == 1:
    #             if "_" not in query_.first().fq_number:
    #                 obj.fq_number = query_.first().fq_number + "_1"
    #         elif query_.count() > 1:
    #             index = 0
    #             if "_" not in query_.first():
    #                 a = query_.first().fq_number
    #             else:
    #                 a = query_.first().fq_number.split("_")[0]
    #             for i in query_:
    #                 if "_" in i.bs_number:
    #                     if index < int(i.bs_number[-1]):
    #                         index = int(i.bs_number[-1])
    #             obj.fq_number = a + "_" + str(
    #                 index + 1)
    #         else:
    #             qr = ExtExecute.objects.filter(boxes=box)
    #             if qr.count() == 0:
    #                 err = "该样本还未经过提取，请核对"
    #                 obj.fq_number = err
    #             else:
    #                 for i in qr:
    #                     if "_" not in i.ext_number:
    #                         number = i.ext_number
    #                         obj.fq_number = number
    #         if not obj.fq_number:
    #             obj.fq_number = "未找到该样本"
    #     if obj.status == 1:
    #         ResultJudgement.objects.create(boxes=obj.boxes, fq=obj)
    #         box = form.cleaned_data["boxes"]
    #         if box.status < 6:
    #             box.status = 6
    #             box.save()
    #     else:
    #         pass
    #     obj.save()

    def save_model(self, request, obj, form, change):
        # if form.cleaned_data["boxes"]:
        #     box = form.cleaned_data["boxes"]
        # else:
        box = obj.boxes
        query_ext = ExtExecute.objects.filter(boxes=box)
        query_qua = QualityTest.objects.filter(boxes=box)
        query_bs = BsTask.objects.filter(boxes=box)
        # query_flu = FluorescenceQuantification.objects.filter(boxes=box)
        if not obj.fq_number:
            obj.ext_times = query_ext.count()
            obj.qua_times = query_qua.count()
            obj.bs_times = query_bs.count()
            obj.fq_number = query_ext.first().qua_number
        if obj.submit:
            if obj.status == 1:
                ExtExecute.objects.create(boxes=box,
                                          ext_number=
                                          query_qua.first().ext_number,
                                          ext_times=query_ext.count() + 1)
                if box.status < 2:
                    box.update(status=2)
            elif obj.status == 2:
                QualityTest.objects.create(qua_number=obj.fq_number,
                                           boxes=box,
                                           ext_times=form.cleaned_data[
                                               "ext_times"],
                                           qua_times=query_qua.count() + 1)
                if box.status < 4:
                    box.status = 4
                    box.save()
            elif obj.status == 3:
                BsTask.objects.create(
                    bs_number=obj.fq_number,
                    boxes=box,
                    ext_times=form.cleaned_data[
                        "ext_times"],
                    qua_times=form.cleaned_data[
                        "qua_times"],
                    bs_times=query_qua.count() + 1)
                if box.status < 6:
                    box.status = 6
                    box.save()
            elif obj.status == 4:
                ext_ = ExtExecute.objects.filter(boxes=box).count()
                ext = ExtExecute.objects.filter(Q(boxes=box),
                                                Q(ext_times=ext_))
                ResultJudgement.objects.create(
                    boxes=obj.boxes, fq=obj, ext=ext.first())
                if box.status < 10:
                    box.status = 10
                    box.save()
            else:
                pass
        else:
            pass
        if box.status < 9:
            box.status = 9
            box.save()
        obj.save()


class ResultJudgementAdmin(admin.ModelAdmin):
    list_per_page = 50
    search_fields = ["boxes", ]
    save_on_top = False
    list_display = (
        "boxes", 'rj_date', 'fq_operator', "status"
    )
    list_display_links = ('boxes',)
    autocomplete_fields = ("boxes",)
    readonly_fields = ["boxes", "fq_date", "fq_operator", "fq_instrument",
                       "fq_actb_ct", "fq_actb_amp", "fq_sfrp2_ct",
                       "fq_sfrp2_amp", "fq_sdc2_ct", "fq_sdc2_amp",
                       "fq_is_qualified", "ext_hemoglobin", "result", 'judge',
                       "rj_date"]
    fieldsets = (
        ('实验相关信息', {
            'fields': ('boxes', 'judge', "result", "rj_date")
        }),
        ('血红蛋白', {
            'fields': ('ext_hemoglobin',)
        }),
        ('荧光定量', {
            'fields': (("fq_date", "fq_operator", "fq_instrument"),
                       ("fq_actb_ct", "fq_actb_amp"), ("fq_sfrp2_ct",
                                                       "fq_sfrp2_amp"),
                       ("fq_sdc2_ct", "fq_sdc2_amp"),
                       "fq_is_qualified",)
        }),
        ('结果判定', {
            'fields': ("status", "submit")
        }),
    )

    def ext_hemoglobin(self, obj):
        if obj.ext.hemoglobin:
            return obj.ext.hemoglobin
        else:
            return "-"

    ext_hemoglobin.short_description = '血红蛋白'

    def fq_date(self, obj):
        if obj.fq.fq_date:
            return obj.fq.fq_date
        else:
            return "-"

    fq_date.short_description = '荧光定量日期'

    def fq_operator(self, obj):
        if obj.fq.operator:
            return obj.fq.operator
        else:
            return "-"

    fq_operator.short_description = '荧光定量实验员'

    def fq_instrument(self, obj):
        if obj.fq.instrument:
            return obj.fq.instrument
        else:
            return "-"

    fq_instrument.short_description = '荧光定量仪器'

    def fq_actb_ct(self, obj):
        if obj.fq.actb_ct:
            return obj.fq.actb_ct
        else:
            return "-"

    fq_actb_ct.short_description = '荧光定量-actb_ct'

    def fq_actb_amp(self, obj):
        if obj.fq.actb_amp:
            return obj.fq.actb_amp
        else:
            return "-"

    fq_actb_amp.short_description = '荧光定量-actb_amp'

    def fq_sfrp2_ct(self, obj):
        if obj.fq.sfrp2_ct:
            return obj.fq.sfrp2_ct
        else:
            return "-"

    fq_sfrp2_ct.short_description = '荧光定量-sfrp2_ct'

    def fq_sfrp2_amp(self, obj):
        if obj.fq.sfrp2_amp:
            return obj.fq.sfrp2_amp
        else:
            return "-"

    fq_sfrp2_amp.short_description = '荧光定量-sfrp2_amp'

    def fq_sdc2_ct(self, obj):
        if obj.fq.sdc2_ct:
            return obj.fq.sdc2_ct
        else:
            return "-"

    fq_sdc2_ct.short_description = '荧光定量-sdc2_ct'

    def fq_sdc2_amp(self, obj):
        if obj.fq.sdc2_amp:
            return obj.fq.sdc2_amp
        else:
            return "-"

    fq_sdc2_amp.short_description = '荧光定量-sdc2_amp'

    def fq_is_qualified(self, obj):
        if obj.fq.is_qualified:
            return obj.fq.is_qualified
        else:
            return "-"

    fq_is_qualified.short_description = '荧光定量-is_qualified'

    def save_model(self, request, obj, form, change):
        if obj.result and obj.rj_date and not obj.status:
            obj.status = 1
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "judge":
            saler_ = BmsUser.objects.filter(groups__name="实验总监")
            kwargs["queryset"] = saler_
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.submit:
                return ["boxes", "fq_date", "fq_operator", "fq_instrument",
                        "fq_actb_ct", "fq_actb_amp", "fq_sfrp2_ct",
                        "fq_sfrp2_amp", "fq_sdc2_ct", "fq_sdc2_amp",
                        "fq_is_qualified", "ext_hemoglobin", "result", 'judge',
                        "rj_date", "status", "submit"]
            current_group_set = Group.objects.filter(user=request.user)
            if len(current_group_set) == 1:
                if current_group_set[0].name == "技术支持":
                    return self.readonly_fields
                elif current_group_set[0].name == "实验总监" and obj.status:
                    return ["boxes", "fq_date", "fq_operator", "fq_instrument",
                            "fq_actb_ct", "fq_actb_amp", "fq_sfrp2_ct",
                            "fq_sfrp2_amp", "fq_sdc2_ct", "fq_sdc2_amp",
                            "fq_is_qualified", "ext_hemoglobin", 'judge',
                            "status", "submit", "rj_date", "result"]
                elif current_group_set[0].name == "实验总监" and not obj.status:
                    return ["boxes", "fq_date", "fq_operator", "fq_instrument",
                            "fq_actb_ct", "fq_actb_amp", "fq_sfrp2_ct",
                            "fq_sfrp2_amp", "fq_sdc2_ct", "fq_sdc2_amp",
                            "fq_is_qualified", "ext_hemoglobin", 'judge',
                            "status", "submit"]
                else:
                    return self.readonly_fields
            else:
                names = [i.name for i in current_group_set]
                if "技术支持" in names:
                    return self.readonly_fields
                elif "实验总监" in names:
                    return ["boxes", "fq_date", "fq_operator", "fq_instrument",
                            "fq_actb_ct", "fq_actb_amp", "fq_sfrp2_ct",
                            "fq_sfrp2_amp", "fq_sdc2_ct", "fq_sdc2_amp",
                            "fq_is_qualified", "ext_hemoglobin", 'judge',
                            "status", "submit"]
                else:
                    return self.readonly_fields
        except AttributeError:
            pass
        return self.readonly_fields
