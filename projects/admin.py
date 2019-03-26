import datetime
# import json

from django.utils.html import format_html
# from django.contrib.auth.models import Group
# from django.http import JsonResponse, HttpResponse
# from django.urls import path
# from django.db.models import Q

from projects.models import ContractsInfo, InvoiceInfo
from projects.forms import ContractInfoForm, InvoiceInfoForm
from projects.resources import ContractInfoResources, InvoiceInfoResources
from import_export.admin import ImportExportActionModelAdmin
from invoices.models import SendInvoices, PaymentInfo
# from accounts.models import BmsUser
# from projects import views


class ContractsInfoAdmin(ImportExportActionModelAdmin):
    """合同信息管理"""
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
        receive_value = 0
        payment_datas = PaymentInfo.objects.filter(contract_number=obj.id,
                                                   receive_value__isnull=False)
        if payment_datas is not None:
            for payment in payment_datas:
                receive_value += payment.receive_value
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
            contract_code = datetime.datetime.now().strftime('%Y%m%d') + \
                            'RYS-' + datetime.datetime.now().strftime('%H%M%S')
            obj.contract_code = contract_code
            super().save_model(request, obj, form, change)


class InvoiceInfoAdmin(ImportExportActionModelAdmin):
    """开票信息管理"""

    change_form_template = 'admin/projects/projects_invoices_change_form.html'
    fields = ('contract_id', 'salesman', 'invoice_type', 'invoice_issuing',
              'invoice_title', 'tariff_item', 'send_address',
              'address_phone', 'opening_bank', 'bank_account_number',
              'invoice_value', 'invoice_content', 'remark', 'apply_name',
              'flag', 'approve_flag',)
    # TODO:发票提交、审批按钮按权限显示（测试）
    # base_fields = ('contract_id', 'salesman', 'invoice_type',
    #                'invoice_issuing', 'invoice_title', 'tariff_item',
    #                'send_address', 'address_phone', 'opening_bank',
    #                'bank_account_number', 'invoice_value', 'invoice_content',
    #                'remark', 'apply_name',
    #           )
    list_display = (
        'salesman', 'invoice_title', 'invoice_value', 'invoice_type',
        'invoice_content', 'flag', 'approve_flag',
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
        # TODO: 由发票状态和用户权限确定只读字段
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
        # TODO:发票提交、审批按钮按权限显示（测试）
        # condition = Q(groups__id=2) & Q(id=request.user.id)
        # current_user = BmsUser.objects.filter(condition).all()
        # self.fields = []
        # if current_user.exists():
        #     print(current_user)
        #     self.fields = self.base_fields + ('approve_flag',)
        # else:
        #     self.fields = self.base_fields + ('flag',)
        return super(InvoiceInfoAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def save_model(self, request, obj, form, change):
        """重写model保存函数，保存申请信息，同时新建寄送发票信息记录"""
        if change:
            send_invoices = SendInvoices.objects.filter(invoice_id=obj)
            if not send_invoices.exists():
                approve_status = request.POST.get('approve_flag',
                                                  obj.approve_flag)
                if approve_status == 'tg':
                    value = float(request.POST.get('invoice_value',
                                                   obj.invoice_value))
                    SendInvoices.objects.create(invoice_id=obj, wait_payment=value)
            super(InvoiceInfoAdmin, self).save_model(request, obj, form, change)
        else:
            #新建发票信息
            obj.invoice_number = 'FPID' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            super(InvoiceInfoAdmin, self).save_model(request, obj, form, change)
            if request.POST.get('approve_flag') == 'tg':
                value = float(request.POST.get('invoice_value'))
                SendInvoices.objects.create(invoice_id=obj, wait_payment=value)
