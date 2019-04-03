import datetime
# import json

from django.utils.html import format_html
from django.db.models import Sum
# from django.contrib.auth.models import Group
# from django.http import JsonResponse, HttpResponse
# from django.urls import path

from import_export.admin import ImportExportActionModelAdmin

from projects.models import ContractsInfo
from projects.forms import ContractInfoForm
from projects.resources import ContractInfoResources
from bs_invoices.models import BusinessRecord
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

    def receive_invoice_value(self, obj):
        """自定义列表字段：已到账金额"""
        paid = 0
        bs_record = BusinessRecord.objects.filter(contract_number=obj.id)
        if len(bs_record):
            for record_data in bs_record:
                payment_data = record_data.payment_set.all()
                pay = payment_data.aggregate(value=Sum('receive_value'))
                pay_amount = pay.get('value', 0)
                paid += pay_amount
        return format_html(
            '<span>{}</span>', paid
        )
    receive_invoice_value.short_description = "已到账金额"

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
