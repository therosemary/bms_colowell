# from django.urls import path
# from django.http import JsonResponse, HttpResponse
from django.utils.html import format_html
# import json
from import_export.admin import ImportExportActionModelAdmin
from projects.models import InvoiceInfo, ContractsInfo, BoxApplications
from invoices.models import SendInvoices
from projects.forms import ContractInfoForm, InvoiceInfoForm, BoxApplicationsForm
from projects.resources import ContractInfoResources, InvoiceInfoResources, \
    BoxApplicationsResources
# from projects import views
import  datetime

class ContractsInfoAdmin(ImportExportActionModelAdmin):
    """合同信息管理"""
    # TODO: 20190108 合同信息外键关联代理商和业务员，造成其中一个外键无用
    fields = (
        'contract_number', 'client', 'box_price', 'detection_price',
        'contract_money', 'send_date', 'tracking_number', 'send_back_date',
        'contract_content', 'contract_type', 'start_date', 'end_date',
        'staff_name', 'remark',
    )
    list_display = (
        'contract_code', 'staff_name', 'contract_number', 'contract_type',
        'client', 'box_price', 'detection_price', 'full_set_price',
        'contract_money', 'receive_invoice_value', 'send_date',
        'tracking_number', 'send_back_date', 'start_date', 'end_date',
    )
    list_per_page = 40
    save_as_continue = False
    form = ContractInfoForm
    resource_class = ContractInfoResources
    list_display_links = ('staff_name', 'contract_number', 'contract_code')

    def full_set_price(self, obj):
        """自定义列表字段：单套总价"""
        if (obj.box_price is not None) and (obj.detection_price is not None):
            full_price = obj.box_price + obj.detection_price
        else:
            full_price = '-'
        return format_html(
            '<span>{}</span>', full_price
        )
    full_set_price.short_description = "单套总价"

    # def count_invoice_value(self, obj):
    #     """自定义列表字段：已开票额；包含未审核金额"""
    #     total_value = 0
    #     invoice_datas = InvoiceInfo.objects.filter(
    #         contract_id=obj.contract_id, flag=True
    #     )
    #     if invoice_datas:
    #         for data in invoice_datas:
    #             if data.sendinvoices.invoice_approval_status:
    #                 total_value += data.invoice_value
    #     return format_html(
    #         '<span>{}</span>', total_value
    #     )
    # count_invoice_value.short_description = "已开票金额"

    def receive_invoice_value(self, obj):
        """自定义列表字段：已到账金额"""
        # TODO: 修改开票信息后改
        receive_value = 0
        invoice_datas = InvoiceInfo.objects.filter(contract_id=obj.id)
        if invoice_datas:
            for data in invoice_datas:
                if data.sendinvoices.send_flag and data.receive_value is not None:
                    receive_value += data.receive_value
        return format_html(
            '<span>{}</span>', receive_value
        )
    receive_invoice_value.short_description = "已到账金额"

    def get_readonly_fields(self, request, obj=None):
        """功能：配合change_view()使用，实现合同完成后信息变为只读"""
        self.readonly_fields = ()
        if hasattr(obj, 'end_status'):
            if obj.end_status:
                self.readonly_fields = (
                    'contract_number', 'client', 'staff_name', 'box_price',
                    'detection_price', 'contract_money', 'send_date',
                    'tracking_number', 'send_back_date', 'contract_content',
                    'shipping_status', 'contract_type', 'remark', 'end_status'
                )
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        contract_data = ContractsInfo.objects.filter(id=object_id)
        self.get_readonly_fields(request, obj=contract_data)
        return super(ContractsInfoAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def save_model(self, request, obj, form, change):
        if change:
            super(ContractsInfoAdmin, self).save_model(request, obj, form, change)
        else:
            print(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            contract_code = datetime.datetime.now().strftime('%Y%m%d') + \
                            'RYS-' + datetime.datetime.now().strftime('%H%M%S')
            obj.contract_code = contract_code
            super().save_model(request, obj, form, change)


class InvoiceInfoAdmin(ImportExportActionModelAdmin):
    """开票信息管理"""

    change_form_template = 'admin/projects/projects_invoices_change_form.html'
    fieldsets = (
        (u'开票信息', {
            'fields': ('contract_id', 'salesman', 'invoice_type',
                       'invoice_issuing', 'invoice_title', 'tariff_item',
                       'send_address', 'address_phone', 'opening_bank',
                       'bank_account_number', 'invoice_value', 'invoice_content',
                       'remark', 'apply_name', 'flag',)
        }),
        (u'到账信息', {
            'fields': ('receive_value', 'receive_date',)
        })
    )
    list_display = (
        'salesman', 'invoice_title', 'invoice_value', 'invoice_type',
        'invoice_content', 'receive_value', 'receive_date',
    )
    list_per_page = 40
    save_as_continue = False
    date_hierarchy = "fill_date"
    form = InvoiceInfoForm
    resource_class = InvoiceInfoResources
    list_display_links = ('salesman', 'invoice_title')
    search_fields = ('salesman',)

    # def get_urls(self):
    #     urls = super().get_urls()
    #     ajax_url = [
    #         path(r'add/projects/ajax_salesman/', self.ajax_salesman)
    #     ]
    #     return ajax_url + urls
    #
    # def ajax_salesman(self, request):
    #     """动态获取当前合同对应的业务员"""
    #     self.admin_site.name = 'projects'
    #     print('111111111%s' % request.path)
    #     salesman_result = {'salesamn': 'salesman'}
    #     if request.is_ajax():
    #         contract_val = request.GET['contract_number']
    #         if contract_val is not None:
    #             contract_data = ContractsInfo.objects.get(contract_number=contract_val)
    #             salesman_result = {'salesamn': contract_data['staff_name']}
    #     return JsonResponse(salesman_result)
    #     # return HttpResponse(json.dumps(salesman_result), content_type='application/json')

    def get_readonly_fields(self, request, obj=None):
        """功能：配合change_view()使用，实现申请提交后信息变为只读"""
        self.readonly_fields = ()
        if hasattr(obj, 'flag'):
            if obj.flag:
                self.readonly_fields = (
                    'contract_id', 'salesman', 'invoice_type',
                    'invoice_issuing', 'invoice_title', 'tariff_item',
                    'send_address', 'address_phone', 'opening_bank',
                    'bank_account_number', 'invoice_value', 'invoice_content',
                    'remark', 'apply_name', 'flag',
                )
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        contract_data = InvoiceInfo.objects.filter(id=object_id)
        self.get_readonly_fields(request, obj=contract_data)
        return super(InvoiceInfoAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def save_model(self, request, obj, form, change):
        """重写model保存函数，保存申请信息，同时新建寄送发票信息记录"""
        if change:
            send_invoices = SendInvoices.objects.filter(invoice_id=obj)
            if not send_invoices.exists():
                if request.POST.get('flag'):
                    SendInvoices.objects.create(invoice_id=obj)
            super(InvoiceInfoAdmin, self).save_model(request, obj, form, change)
        else:
            #新建发票信息
            super(InvoiceInfoAdmin, self).save_model(request, obj, form, change)
            if request.POST.get('flag'):
                SendInvoices.objects.create(invoice_id=obj)


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
