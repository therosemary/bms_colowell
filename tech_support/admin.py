import datetime
from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportActionModelAdmin, \
    ExportActionModelAdmin
from django.contrib.admin import ModelAdmin
from tech_support.forms import BoxApplicationsForm
from rangefilter.filter import DateRangeFilter

from tech_support.models import *
from import_export import fields
from tech_support.resources import BoxApplicationsResources
from tech_support.resources import TechsupportResources
    # BoxDeliveriesResource

Monthchoose = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G",
               8: "H", 9: "I", 10: "G", 11: "K", 12: "L", }


# class TechsupportInline(admin.TabularInline):
#     model = Techsupport
#     fields = ["barcode", "name"]
#
#     def get_readonly_fields(self, request, obj=None):
#         try:
#             if obj.submit:
#                 return ["barcode", "name"]
#         except AttributeError:
#             return []
#         return []


# class BoxDeliveriesAdmin(ImportExportActionModelAdmin):
#     """盒子发货管理"""
#     inlines = [TechsupportInline]
#     list_per_page = 50
#     search_fields = ("sale_man", "send_date")
#     save_on_top = False
#     list_display = ("sale_man", "customer",
#                     'send_number', 'send_date', 'made_date')
#     list_display_links = ('customer',)
#     # resource_class = BoxDeliveriesResource
#     fieldsets = (
#         ('盒子发货信息', {
#             'fields': ('sale_man', 'customer', 'send_number',
#                        "address", "box_number",
#                        "send_date", "made_date", 'submit')
#         }),
#     )
#
#     def get_export_resource_class(self):
#         return
#
#     def get_import_resource_class(self):
#         return
#
#     def get_readonly_fields(self, request, obj=None):
#         try:
#             if obj.submit:
#                 return ['sale_man', "customer", "box_number",
#                         "send_number", "send_date",
#                         'made_date', "submit", "index_number", "address"]
#         except AttributeError:
#             pass
#         return ["box_number", ]
#
#     def box_number(self, obj):
#         if obj:
#             n = 0
#             for i in obj.boxes_set.all():
#                 n += 1
#             return n
#         return 0
#     box_number.short_description = '盒子数量'
#
#     def save_model(self, request, obj, form, change):
#         if not obj.index_number:
#             sj = datetime.datetime.now()
#             if BoxDeliveries.objects.all().count() == 0:
#                 obj.index_number = str(sj.year) + Monthchoose[sj.month] + "1"
#
#             else:
#                 obj.index_number = str(sj.year) + Monthchoose[sj.month] + str
#                     (BoxDeliveries.objects.latest('id').id + 1)
#         obj.save()
#
#     def save_formset(self, request, form, formset, change):
#         instances = formset.save(commit=False)
#         for obj in formset.deleted_objects:
#             obj.delete()
#         if instances:
#             sj = datetime.datetime.now()
#             for instance in instances:
#                 # if not instance.index_number:
#                 #     if Techsupport.objects.all().count() == 0:
#                 #         instance.index_number = "HZ" + str(sj.year) + \
#                 #                                 Monthchoose[
#                 #                                     sj.month] + "1"
#                 #     else:
#                 #         instance.index_number = "HZ" + str(sj.year) + \
#                 #                                 Monthchoose[
#                 #                                     sj.month] + str(
#                 #             Techsupport.objects.latest('id').id + 1)
#                 instance.save()
#                 formset.save_m2m()


@admin.register(Techsupport)
class TechsupportAdmin(ImportExportActionModelAdmin):
    """盒子管理"""
    list_per_page = 50
    search_fields = ("send_number", "index_number", "barcode")
    save_on_top = False
    list_display = (
        'index_number', "barcode", 'receive_date', 'name',
    )
    list_display_links = ('barcode',)
    actions = ["accept_box", ]
    resource_class = TechsupportResources

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # extra_context = extra_context or {}
        # extra_context['show_delete'] = False
        # extra_context['show_save_and_continue'] = False
        print(object_id)
        return super().change_view(request, object_id, form_url,
                                   extra_context=extra_context)

    def accept_box(self, request, queryset):
        n = 0
        for obj in queryset:
            if obj.status == 0:
                obj.status = 1
                n += 1
                # sj = datetime.datetime.now()
                # if ExtSubmit.objects.all().count() == 0:
                #     extnumber = str(sj.year) + Monthchoose[
                #         sj.month] + "1"
                # else:
                #     extnumber = str(sj.year) + Monthchoose[
                #         sj.month] + str(
                #         ExtSubmit.objects.latest('id').id + 1)
                # ExtExecute.objects.create(ext_number=extnumber, boxes=obj)
            else:
                pass
        self.message_user(request, "已成功核对{0}个盒子样本".format(n))

    accept_box.short_description = '核对所选盒子'

    def get_list_filter(self, request):
        return ['status',  "insure_receive",
                ('receive_date', DateRangeFilter),
                ('report_end_date', DateRangeFilter)]

    def get_actions(self, request):
        actions = super().get_actions(request)
        current_group_set = Group.objects.filter(user=request.user)
        for i in current_group_set:
            if i.name != "技术支持":
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

    def get_exclude(self, request, obj=None):
        current_group_set = Group.objects.filter(user=request.user)
        for i in current_group_set:
            if i.name != "技术支持":
                return ['accept_box']

    def save_model(self, request, obj, form, change):
        if obj.insure_receive and obj.status == 0:
            obj.status = 1
        obj.save()


class ExtMethodAdmin(ModelAdmin):
    """提取方法管理"""
    list_display = ('method',)


class ExtSubmitAdmin(ImportExportActionModelAdmin):
    """提取下单管理"""
    list_per_page = 50
    save_on_top = False
    list_display = ("ext_date", "exp_method", "submit")
    list_display_links = ("exp_method",)
    filter_horizontal = ("boxes",)

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.submit:
                return ['boxes', "exp_method", "submit"]
        except AttributeError:
            pass
        return []

    def save_model(self, request, obj, form, change):
        # if not obj.extsubmit_number:
        #     sj = datetime.datetime.now()
        #     if ExtSubmit.objects.all().count() == 0:
        #         obj.extsubmit_number = str(sj.year) + Monthchoose[
        #             sj.month] + "1"
        #     else:
        #         obj.extsubmit_number = str(sj.year) + Monthchoose[
        #             sj.month] + str(
        #             ExtSubmit.objects.latest('id').id + 1)
        if obj.submit:
            boxes = form.cleaned_data["boxes"]
            for i in boxes:
                i.istasking = True
                i.save()
                # sj = datetime.datetime.now()
                # # print(BoxDeliveries.objects.all().count())
                # if ExtExecute.objects.all().count() == 0:
                #     ext_number = str(sj.year) + Monthchoose[
                #         sj.month] + "1".zfill(5)
                #
                # else:
                #     ext_number = str(sj.year) + Monthchoose[
                #         sj.month] + str(
                #         ExtExecute.objects.latest('id').id + 1).zfill(5)
                # ExtExecute.objects.create(ext_number=ext_number, boxes=i)
        obj.save()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "boxes":
            kwargs["queryset"] = Techsupport.objects.filter(istasking=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class BoxApplicationsAdmin(ImportExportActionModelAdmin):
    """申请盒子信息管理"""

    fields = (
        'contract_number', 'amount', 'classification', 'intention_client',
        'address_name', 'address_phone', 'send_address', 'box_price',
        'detection_price', 'use', 'proposer', 'box_submit_flag'
    )
    list_display = (
        'colored_contract_number', 'amount', 'classification',
        'intention_client', 'address_name', 'address_phone', 'send_address',
        'proposer', 'box_price', 'detection_price', 'use', 'submit_time',
        'approval_status', 'box_submit_flag'
    )
    list_per_page = 40
    save_as_continue = False
    resource_class = BoxApplicationsResources
    form = BoxApplicationsForm

    def get_readonly_fields(self, request, obj=None):
        """功能：配合change_view()使用，实现申请提交后信息变为只读"""
        self.readonly_fields = ()
        if hasattr(obj, 'box_submit_flag'):
            if obj.box_submit_flag:
                self.readonly_fields = (
                    'contract_number', 'amount', 'classification',
                    'intention_client', 'address_name', 'address_phone',
                    'send_address', 'box_price', 'detection_price', 'use',
                    'box_submit_flag'
                )
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        contract_data = BoxApplications.objects.filter(id=object_id)
        self.get_readonly_fields(request, obj=contract_data)
        return super(BoxApplicationsAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['proposer'] = request.user
        return initial
