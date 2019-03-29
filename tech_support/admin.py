import datetime
from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse
from import_export.admin import ImportExportActionModelAdmin, \
    ExportActionModelAdmin
from django.contrib.admin import ModelAdmin

from accounts.models import BmsUser, DingtalkInfo
from tech_support.forms import BoxApplicationsForm
from rangefilter.filter import DateRangeFilter
from tech_support.models import *
from tech_support.resources import BoxApplicationsResources
from tech_support.resources import TechsupportResources
from django.contrib import admin
from django.urls import reverse
from bms_colowell.utils import InlineImportExportModelAdmin
from bms_colowell.mixins import NotificationMixin
from bms_colowell.settings import DINGTALK_APPKEY, DINGTALK_SECRET, \
    DINGTALK_AGENT_ID


Monthchoose = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G",
               8: "H", 9: "I", 10: "G", 11: "K", 12: "L", }


class TechsupportInline(admin.TabularInline):
    model = Techsupport
    fields = ["barcode", "name"]

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.submit:
                return ["barcode", "name"]
        except AttributeError:
            return []
        return []


class BoxDeliveriesAdmin(ModelAdmin):
    """盒子发货管理"""
    inlines = [TechsupportInline]
    list_per_page = 50
    search_fields = ("bd_number", "sale_man", "send_date")
    save_on_top = False
    list_display = ("bd_number", "contract_number", "sale_man", "customer",
                    'send_number', 'send_date', 'made_date')
    list_display_links = ("bd_number", "contract_number")
    # resource_class = BoxDeliveriesResource
    fieldsets = (
        ('盒子发货信息', {
            'fields': ('sale_man', "contract_number", 'customer',
                       'send_number', "address", "appl_number", "box_number",
                       "send_date", "made_date", 'submit')
        }),
    )

    @staticmethod
    def _get_model_info(model):
        return model._meta.app_label, model._meta.model_name

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Reconstruct the change view in order to pass inline import data for
        current model admin."""

        extra_context = extra_context or {}

        # Get all inline model and prepare context for each of them.
        inline_import_urls = []
        for inline_model in self.inlines:
            model_info = self._get_model_info(inline_model.model)
            redirect_url = reverse("admin:{}_{}_import".format(*model_info))
            verbose_name = inline_model.model._meta.verbose_name

            model_info_dict = {"verbose_name": verbose_name,
                               "redirect_url": redirect_url, }
            inline_import_urls.append(model_info_dict)

        # TODO: The redirection after import should be handled.
        # current_model_info = self._get_model_info(self.model)
        # whole_url_name = "admin:{}_{}_changelist".format(*current_model_info)
        # redirect_to = reverse(whole_url_name)
        # request.session["redirect_to"] = redirect_to

        # To store the primary key of the model into request.session, bring
        # this state to the import view of inline model
        # TODO: to deal with the session pollution
        pk_name = "{}_id".format(self.model._meta.pk.attname)
        request.session[pk_name] = object_id
        request.session["inline_import"] = True

        # refresh the context
        extra_context["inline_import_urls"] = inline_import_urls
        return super().change_view(request, object_id,
                                   extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.submit:
                return ['sale_man', "customer", "box_number", "sale_man",
                        "contract_number", "send_number", "send_date",
                        "appl_number", 'made_date', "submit", "index_number",
                        "address"]
        except AttributeError:
            pass
        return ["box_number", "appl_number", "contract_number", "sale_man"]

    def box_number(self, obj):
        if obj:
            n = Techsupport.objects.filter(bd_number=obj).count()
            return n
        return 0

    box_number.short_description = '现有盒子数量'

    def save_model(self, request, obj, form, change):
        if not obj.bd_number:
            sj = datetime.datetime.now()
            if BoxDeliveries.objects.all().count() == 0:
                obj.bd_number = str(sj.year) + Monthchoose[sj.month] + "1"

            else:
                obj.bd_number = str(sj.year) + Monthchoose[sj.month] + str(
                    BoxDeliveries.objects.latest('id').id + 1)
        if not obj.sale_man:
            obj.sale_man = request.user
        obj.save()

    # def save_formset(self, request, form, formset, change):
    #     instances = formset.save(commit=False)
    #     for obj in formset.deleted_objects:
    #         obj.delete()
    #     if instances:
    #         for instance in instances:
    #             instance.save()
    #             boxdeliever = instance.bd_number
    #             boxdeliever.box_number += 1
    #             boxdeliever.save()
    #             formset.save_m2m()


@admin.register(Techsupport)
class TechsupportAdmin(InlineImportExportModelAdmin):
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
        return ['status', "insure_receive",
                ('receive_date', DateRangeFilter),
                ('report_end_date', DateRangeFilter)]

    def get_actions(self, request):
        actions = super().get_actions(request)
        current_group_set = Group.objects.filter(user=request.user)
        for i in current_group_set:
            if i.name != "技术支持":
                del actions['accept_box']
        return actions

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


class BoxApplicationsAdmin(ImportExportActionModelAdmin, NotificationMixin):
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
    appkey = DINGTALK_APPKEY
    appsecret = DINGTALK_SECRET
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

    def save_model(self, request, obj, form, change):
        if obj.box_submit_flag:
            sj = datetime.datetime.now()
            if BoxDeliveries.objects.all().count() == 0:
                bd_number = str(sj.year) + Monthchoose[sj.month] + "1"
            else:
                bd_number = str(sj.year) + Monthchoose[sj.month] + str(
                        BoxDeliveries.objects.all().count() + 1)
            BoxDeliveries.objects.create(appl_number=obj.amount,
                                         contract_number=obj.contract_number,
                                         bd_number=bd_number)
            content = "合同{}的盒子申请提交成功".format(obj.contract_number)
            tech = []
            for i in BmsUser.objects.all():
                if i.has_perm("tech_support.change_boxapplications"):
                    ding_ = DingtalkInfo.objects.filter(bms_user=i).first()
                    if ding_:
                        dingid = ding_.userid
                    else:
                        dingid = None
                    tech.append(dingid)
            self.send_work_notice(content, DINGTALK_AGENT_ID,
                                  tech)
            call_back = self.send_dingtalk_result
            message = "已钉钉通知" if call_back else "钉钉通知失败"
            self.message_user(request, message)
        obj.save()