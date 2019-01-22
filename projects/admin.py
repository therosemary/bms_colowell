import datetime
import random
import re

from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from import_export.fields import Field
from projects.models import InvoiceInfo, ContractsInfo, BoxApplications
from invoices.models import SendInvoices
from projects.forms import ContractInfoForm, InvoiceInfoForm


def make_contract_id():
    """时间+随机生成数组合为合同编号"""
    now_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    number = str(random.randint(1, 10000))
    return 'YX' + now_datetime + str(number)


class ContractInfoResources(resources.ModelResource):
    full_set_price = Field(
        column_name="全套价格",
    )
    count_invoice_value = Field(
        column_name="已开票金额"
    )
    receive_invoice_value = Field(
        column_name="已到账金额"
    )

    class Meta:
        model = ContractsInfo
        fields = (
            'contract_number', 'client', 'staff_name', 'box_price',
            'detection_price', 'full_set_price', 'contract_money',
            'count_invoice_value', 'receive_invoice_value', 'send_date',
            'tracking_number', 'send_back_date', 'shipping_status',
            'contract_type', 'end_status'
        )
        export_order = (
            'contract_number', 'client', 'staff_name', 'box_price',
            'detection_price', 'full_set_price', 'contract_money',
            'count_invoice_value', 'receive_invoice_value', 'send_date',
            'tracking_number', 'send_back_date', 'shipping_status',
            'contract_type', 'end_status'
        )
        skip_unchanged = True

    def get_export_headers(self):
        export_headers = [u'合同号', u'客户', u'业务员', u'盒子单价', u'检测单价',
                          u'全套价格', u'合同金额', u'已开票额', u'已到账额',
                          u'合同寄出时间', u'邮件单号', u'合同寄回时间', u'发货状态',
                          u'合同类型', u'是否完结']
        return export_headers

    def dehydrate_full_set_price(self, contractinfo):
        full_set_price = contractinfo.box_price + contractinfo.detection_price
        return full_set_price

    def dehydrate_count_invoice_value(self, contractinfo):
        """获取已开票总额，包含未审核金额"""
        total_value = 0
        invoice_datas = InvoiceInfo.objects.filter(
            contract_id=contractinfo.contract_id, flag=True
        )
        if invoice_datas:
                for data in invoice_datas:
                    if data.sendinvoices.invoice_approval_status:
                        total_value += data.invoice_value
        return total_value

    def dehydrate_receive_invoice_value(self, contractinfo):
        """获取已到账总金额"""
        receive_value = 0
        invoice_datas = InvoiceInfo.objects.filter(contract_id=contractinfo.contract_id)
        if invoice_datas:
            for data in invoice_datas:
                if data.sendinvoices.invoice_flag:
                    receive_value += data.invoice_value
        return receive_value


class InvoiceInfoResources(resources.ModelResource):
    """发票信息导入导出"""

    contract_number = Field(
        column_name="合同号", attribute='contract_id__contract_number',
    )
    approval_status = Field(
        column_name="审批状态", attribute='sendinvoices__invoice_approval_status'
    )

    class Meta:
        model = InvoiceInfo
        fields = (
            'contract_number', 'cost_type', 'invoice_title', 'tariff_item',
            'invoice_value', 'tax_rate', 'invoice_issuing', 'receive_date',
            'receivables', 'address_name', 'address_phone', 'send_address',
            'apply_name', 'remark', 'flag', 'approval_status'
        )
        export_order = fields
        skip_unchanged = True

    def get_export_headers(self):
        export_headers = [u'合同号', u'发票类型', u'发票抬头', u'税号', u'开票金额',
                          u'税率', u'开票单位', u'到账日期', u'应收金额', u'收件人姓名',
                          u'收件人号码', u'寄送地址', u'申请人', u'备注', '是否提交',
                          u'审批状态']
        return export_headers


class BoxApplicationsResources(resources.ModelResource):
    """盒子申请信息导入导出"""

    contract_number = Field(
        column_name="合同号", attribute='contract_id__contract_number',
    )

    class Meta:
        model = BoxApplications
        fields = (
            'contract_number', 'amount', 'classification', 'address_name',
            'address_phone', 'send_address', 'box_price', 'detection_price',
            'use', 'box_submit_flag'
        )
        export_order = (
            'contract_number', 'amount', 'classification', 'address_name',
            'address_phone', 'send_address', 'box_price', 'detection_price',
            'use', 'box_submit_flag'
        )

    def get_export_headers(self):
        export_headers = [u'合同号', u'申请数量', u'申请类别', u'收件人姓名',
                          u'收件人号码', u'邮寄地址', u'盒子单价', u'用途',
                          u'是否提交']
        return export_headers


class ContractsInfoAdmin(ImportExportActionModelAdmin):
    """合同信息管理"""
    # TODO: 20190108 合同信息外键关联代理商和业务员，造成其中一个外键无用
    fields = (
        'contract_number', 'client', 'staff_name', 'box_price',
        'detection_price', 'contract_money', 'send_date', 'tracking_number',
        'send_back_date', 'contract_content', 'shipping_status',
        'contract_type', 'remark', 'end_status'
    )
    list_display = (
        'contract_number', 'client', 'staff_name', 'box_price',
        'detection_price', 'full_set_price', 'contract_money',
        'count_invoice_value', 'receive_invoice_value', 'send_date',
        'tracking_number', 'send_back_date', 'shipping_status',
        'contract_type', 'end_status'
    )
    list_per_page = 40
    save_as_continue = False
    form = ContractInfoForm
    resource_class = ContractInfoResources

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
                if data.sendinvoices.invoice_approval_status:
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
        contract_data = ContractsInfo.objects.filter(contract_id=object_id)
        self.get_readonly_fields(request, obj=contract_data)
        return super(ContractsInfoAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def save_model(self, request, obj, form, change):
        """重写合同信息保存
        """
        if change:
            super(ContractsInfoAdmin, self).save_model(request, obj, form, change)
        else:
            obj.contract_id = make_contract_id()
            obj.save()

class InvoiceInfoAdmin(ImportExportActionModelAdmin):
    """申请发票信息管理"""
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
        'remark', 'apply_name', 'fill_date', 'flag',
        'get_invoice_approval_status',
    )
    list_per_page = 40
    save_as_continue = False
    date_hierarchy = "fill_date"
    form = InvoiceInfoForm
    resource_class = InvoiceInfoResources

    def get_invoice_approval_status(self, obj):
        if obj.sendinvoices.invoice_approval_status is None:
            status_value = "审核中"
        elif obj.sendinvoices.invoice_approval_status:
            status_value = "通过"
        else:
            status_value = "未通过"
        return status_value
    get_invoice_approval_status.short_description = "审批状态"

    def get_readonly_fields(self, request, obj=None):
        """功能：配合change_view()使用，实现申请提交后信息变为只读"""
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
        """重写model保存函数，保存申请信息，同时新建寄送发票信息记录"""
        if change:
            send_invoices = SendInvoices.objects.filter(invoice_id=obj)
            if not send_invoices.exists():
                if request.POST.get('flag'):
                    SendInvoices.objects.create(invoice_id=obj)
            super(InvoiceInfoAdmin, self).save_model(request, obj, form, change)
        else:
            obj.invoice_id = make_contract_id()
            obj.apply_name = re.search(r'[^【].*[^】]', str(request.user))[0]
            #新建保存开票邮寄信息
            if request.POST.get('flag'):
                SendInvoices.objects.create(invoice_id=obj)
            super(InvoiceInfoAdmin, self).save_model(request, obj, form, change)


class BoxApplicationsAdmin(ImportExportActionModelAdmin):
    """申请盒子信息管理"""
    fields = (
        'contract_id', 'amount', 'classification', 'address_name',
        'address_phone', 'send_address', 'box_price', 'detection_price',
        'use', 'box_submit_flag'
    )
    list_display = (
        'colored_contract_number', 'amount', 'classification', 'address_name',
        'address_phone', 'send_address', 'proposer', 'box_price',
        'detection_price', 'use', 'approval_status', 'box_submit_flag'
    )
    list_per_page = 40
    save_as_continue = False
    resource_class = BoxApplicationsResources

    def get_readonly_fields(self, request, obj=None):
        """功能：配合change_view()使用，实现申请提交后信息变为只读"""
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
