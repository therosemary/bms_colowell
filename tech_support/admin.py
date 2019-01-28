import datetime

from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportActionModelAdmin
from django.contrib.admin import ModelAdmin
from tech_support.models import *
from experiment.models import ExtExecute

Monthchoose = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G",
               8: "H", 9: "I", 10: "G", 11: "K", 12: "L", }


class BoxesInline(admin.TabularInline):
    model = Boxes
    fields = ["bar_code", "name", "type", "projec_source", "is_danger"]

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.submit:
                self.readonly_fields = ["bar_code", "name", "type",
                                        "projec_source", "is_danger"]
        except AttributeError :
            self.readonly_fields = []
            return self.readonly_fields
        return self.readonly_fields


class BoxDeliveriesAdmin(ImportExportActionModelAdmin):
    """盒子发货管理"""
    inlines = [BoxesInline]
    list_per_page = 50
    search_fields = ("sale_man", "send_date")
    save_on_top = False
    list_display = ('index_number', "sale_man", "customer",
                    'send_number', 'send_date', 'made_date')
    list_display_links = ('index_number',)
    exclude = ["index_number", ]

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.submit:
                self.readonly_fields = ['sale_man', "customer", "box_number",
                                        "send_number", "send_date",
                                        'made_date', "submit"]
                return self.readonly_fields
        except AttributeError:
            self.readonly_fields = []
            return self.readonly_fields
        self.readonly_fields = []
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not obj.index_number:
            sj = datetime.datetime.now()
            if BoxDeliveries.objects.all().count() == 0:
                obj.index_number = str(sj.year) + Monthchoose[sj.month] + "1"

            else:
                obj.index_number = str(sj.year) + Monthchoose[sj.month] + str(
                    BoxDeliveries.objects.latest('id').id + 1)
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        if instances:
            sj = datetime.datetime.now()
            for instance in instances:
                if not instance.index_number:
                    if Boxes.objects.all().count() == 0:
                        instance.index_number = "HZ" + str(sj.year) + \
                                                Monthchoose[
                                                    sj.month] + "1"
                    else:
                        instance.index_number = "HZ" + str(sj.year) + \
                                                Monthchoose[
                                                    sj.month] + str(
                            Boxes.objects.latest('id').id + 1)
                    instance.save()
                formset.save_m2m()


class BoxesAdmin(ImportExportActionModelAdmin):
    """盒子管理"""
    list_per_page = 50
    search_fields = ("status", "report_date")
    save_on_top = False
    list_display = (
        'index_number', "bar_code", 'type', 'status',
        'report_date'
    )
    list_display_links = ('index_number',)
    actions = ["accept_box", ]

    def accept_box(self, request, queryset):
        n = 0
        for obj in queryset:
            if obj.status == 0:
                obj.status = 1
                n += 1
                sj = datetime.datetime.now()
                if ExtSubmit.objects.all().count() == 0:
                    extnumber = str(sj.year) + Monthchoose[
                        sj.month] + "1"
                else:
                    extnumber = str(sj.year) + Monthchoose[
                        sj.month] + str(
                        ExtSubmit.objects.latest('id').id + 1)
                ExtExecute.objects.create(ext_number=extnumber, boxes=obj)
            else:
                pass
        self.message_user(request, "已成功核对{0}个盒子样本".format(n))
    accept_box.short_description = '核对所选盒子'

    def get_actions(self, request):
        actions = super().get_actions(request)
        current_group_set = Group.objects.filter(user=request.user)
        for i in current_group_set:
            if i.name == "技术支持":
                del actions['accept_box']
        return actions
        # try:
        #     current_group_set = Group.objects.filter(user=request.user)
        #     # names = [i.name for i in current_group_set]
        #     if current_group_set[0].name == "合作伙伴":
        #         # del actions['export_admin_action']
        #         return actions
        #     else:
        #         # del actions['export_admin_action']
        #         # del actions['make_sampleinfoform_submit']
        #         del actions['insure_sampleinfoform']
        #         # del actions['test1']
        #         return actions
        # except:
        #     return actions


class ExtMethodAdmin(ModelAdmin):
    """提取方法管理"""
    list_display = ('method',)


class ExtSubmitAdmin(ImportExportActionModelAdmin):
    """提取下单管理"""
    list_per_page = 50
    save_on_top = False
    list_display = ("extsubmit_number", 'boxes', "exp_method",)
    list_display_links = ('extsubmit_number',)
    exclude = ["extsubmit_number",]

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.submit:
                self.readonly_fields = ["extsubmit_number", 'boxes',
                                        "exp_method", "submit"]
                return self.readonly_fields
        except AttributeError:
            self.readonly_fields = []
            return self.readonly_fields
        self.readonly_fields = []
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not obj.extsubmit_number:
            sj = datetime.datetime.now()
            if ExtSubmit.objects.all().count() == 0:
                obj.extsubmit_number = str(sj.year) + Monthchoose[
                    sj.month] + "1"
            else:
                obj.extsubmit_number = str(sj.year) + Monthchoose[
                    sj.month] + str(
                    ExtSubmit.objects.latest('id').id + 1)
        obj.save()
