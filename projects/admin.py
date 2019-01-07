from django.contrib import admin
from django.utils.html import format_html
import datetime
import random
from .models import InvoiceInfo, ContractsInfo, BoxApplications
from invoices.models import SendInvoices
import re


def make_contract_id():
    """时间+随机生成数组合为合同编号"""
    now_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    number = str(random.randint(1, 10000))
    return 'YX' + now_datetime + str(number)


class ContractsInfoAdmin(admin.ModelAdmin):
    fields = (
        'contract_number', 'client', 'staff_name', 'box_price',
        'detection_price', 'contract_money', 'send_date', 'tracking_number',
        'send_back_date', 'contract_content', 'shipping_status',
        'contract_type', 'remark', 'end_status'
    )
    list_display = (
        'contract_id', 'contract_number', 'client', 'staff_name',
        'box_price', 'detection_price', 'full_set_price', 'contract_money',
        'count_invoice_value', 'receive_invoice_value', 'send_date',
        'tracking_number', 'send_back_date', 'contract_content',
        'shipping_status', 'contract_type', 'remark', 'end_status'
    )
    list_per_page = 40
    save_as_continue = False

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

    def count_invoice_value(self, obj):
        """自定义列表字段：已开票额；包含未审核金额"""
        total_value = 0
        invoice_datas = InvoiceInfo.objects.filter(
            contract_id=obj.contract_id, flag=True
        )
        if invoice_datas:
            for data in invoice_datas:
                total_value += data.invoice_value
        return format_html(
            '<span>{}</span>', total_value
        )
    count_invoice_value.short_description = "已开票金额"

    def receive_invoice_value(self, obj):
        """自定义列表字段：已到账金额"""
        receive_value = 0
        invoice_datas = InvoiceInfo.objects.filter(contract_id=obj.contract_id)
        if invoice_datas:
            for data in invoice_datas:
                if data.sendinvoices.invoice_flag:
                    receive_value += data.invoice_value
        return format_html(
            '<span>{}</span>', receive_value
        )
    receive_invoice_value.short_description = "已到账金额"

    def get_readonly_fields(self, request, obj=None):
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
        contract_data = ContractsInfo.objects.filter(contract_id=object_id)
        self.get_readonly_fields(request, obj=contract_data)
        return super(ContractsInfoAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def save_model(self, request, obj, form, change):
        if change:
            super(ContractsInfoAdmin, self).save_model(request, obj, form,
                                                       change)
        else:
            obj.contract_id = make_contract_id()
            obj.save()


class InvoiceInfoAdmin(admin.ModelAdmin):
    fields = (
        'contract_id', 'cost_type', 'invoice_title', 'tariff_item',
        'invoice_value', 'tax_rate', 'invoice_issuing', 'receive_date',
        'receivables', 'address_name', 'address_phone', 'send_address',
        'remark', 'flag'
    )
    list_display = (
        'contract_id', 'cost_type', 'invoice_title', 'tariff_item',
        'invoice_value', 'tax_rate', 'invoice_issuing', 'receive_date',
        'receivables', 'address_name', 'address_phone', 'send_address',
        'remark', 'apply_name', 'fill_date', 'flag', 'invoice_approval_status'
    )
    list_per_page = 40
    save_as_continue = False

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ()
        if hasattr(obj, 'flag'):
            if obj.flag:
                self.readonly_fields = (
                    'contract_id', 'cost_type', 'invoice_title', 'tariff_item',
                    'invoice_value', 'tax_rate', 'invoice_issuing',
                    'receive_date', 'receivables', 'address_name',
                    'address_phone', 'send_address', 'remark', 'flag'
                )
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        contract_data = InvoiceInfo.objects.filter(invoice_id=object_id)
        self.get_readonly_fields(request, obj=contract_data)
        return super(InvoiceInfoAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def save_model(self, request, obj, form, change):
        if change:
            super(InvoiceInfoAdmin, self).save_model(request, obj, form, change)
        else:
            obj.invoice_id = make_contract_id()
            obj.apply_name = re.search(r'[^【].*[^】]', str(request.user))[0]
            #新建保存开票邮寄信息
            SendInvoices.objects.create(invoice_id=obj)
            super(InvoiceInfoAdmin, self).save_model(request, obj, form, change)


class BoxApplicationsAdmin(admin.ModelAdmin):
    fields = (
        'contract_id', 'amount', 'classification', 'address_name',
        'address_phone', 'send_address', 'box_price', 'detection_price',
        'use', 'box_submit_flag'
    )
    list_display = (
        'amount', 'classification', 'contract_id', 'address_name',
        'address_phone', 'send_address', 'proposer', 'box_price',
        'detection_price', 'use', 'approval_status', 'box_submit_flag'
    )
    list_per_page = 40
    save_as_continue = False

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ()
        if hasattr(obj, 'box_submit_flag'):
            if obj.box_submit_flag:
                self.readonly_fields = (
                    'contract_id', 'amount', 'classification', 'address_name',
                    'address_phone', 'send_address', 'box_price',
                    'detection_price', 'use', 'box_submit_flag'
                )
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        contract_data = BoxApplications.objects.filter(application_id=object_id)
        self.get_readonly_fields(request, obj=contract_data)
        return super(BoxApplicationsAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def save_model(self, request, obj, form, change):
        if change:
            super(BoxApplicationsAdmin, self).save_model(request, obj, form,
                                                         change)
        else:
            obj.proposer = re.search(r'[^【].*[^】]', str(request.user))[0]
            obj.save()
