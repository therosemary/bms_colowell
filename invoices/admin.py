from django.utils.html import format_html
from import_export.admin import ImportExportActionModelAdmin
from projects.models import InvoiceInfo
from invoices.models import SendInvoices
from invoices.forms import SendInvoicesForm
from invoices.resources import SendInvoiceResources


class SendInvoiceAdmin(ImportExportActionModelAdmin):
    """发票寄送信息管理
       注：每条记录在发票申请提交后自动被创建
    """
    invoice_info = (
        'get_contract_number', 'get_invoice_title', 'get_tariff_item',
        'get_invoice_value', 'get_tax_rate', 'get_invoice_issuing',
        'get_receive_date', 'get_address_name', 'get_address_phone',
        'get_send_address', 'get_apply_name',
    )
    send_invoice_info = (
        'invoice_id', 'invoice_number', 'billing_date', 'invoice_send_date',
        'tracking_number', 'ele_invoice', 'invoice_flag', 'sender', 'send_flag'
    )
    fieldsets = (
        ('发票申请信息', {
            'fields': invoice_info + ('invoice_approval_status',)
        }),
        ('寄送信息填写', {
            'fields': send_invoice_info
        }),
    )
    list_display = (
        'invoice_id', 'get_contract_number', 'get_invoice_title',
        'get_tariff_item', 'get_invoice_value', 'receivables', 'get_tax_rate',
        'get_invoice_issuing', 'get_receive_date', 'get_address_name',
        'get_address_phone', 'get_send_address', 'get_apply_name',
        'invoice_approval_status', 'invoice_number', 'billing_date',
        'invoice_send_date', 'tracking_number', 'ele_invoice', 'invoice_flag',
        'sender', 'fill_name', 'send_flag',
    )
    list_per_page = 40
    save_as_continue = False
    date_hierarchy = 'billing_date'
    readonly_fields = ('invoice_id',) + invoice_info
    form = SendInvoicesForm
    list_filter = ('invoice_id__fill_date', 'invoice_id__apply_name')
    resource_class = SendInvoiceResources

    def receivables(self, obj):
        if obj.invoice_flag:
            money = 0
        else:
            money = self.get_invoice_value(obj)
        return format_html('<span>{}</span>', money)
    receivables.short_description = "应收金额"

    def get_apply_name(self, obj):
        return obj.invoice_id.apply_name
    get_apply_name.short_description = "申请人"

    def get_contract_number(self, obj):
        invoice_data = InvoiceInfo.objects.get(invoice_id=obj.invoice_id)
        if invoice_data.contract_id is not None:
            return invoice_data.contract_id.contract_number
        else:
            return '-'
    get_contract_number.short_description = "合同号"

    def get_invoice_title(self, obj):
        return obj.invoice_id.invoice_title
    get_invoice_title.short_description = "发票抬头"

    def get_tariff_item(self, obj):
        return obj.invoice_id.tariff_item
    get_tariff_item.short_description = "税号"

    def get_invoice_value(self, obj):
        return obj.invoice_id.invoice_value
    get_invoice_value.short_description = "开票金额"

    def get_tax_rate(self, obj):
        return obj.invoice_id.tax_rate
    get_tax_rate.short_description = "税率"

    def get_invoice_issuing(self, obj):
        issuing_entities = {'shry': '上海锐翌', 'hzth': '杭州拓宏', 'hzry': '杭州锐翌'}
        return issuing_entities[obj.invoice_id.invoice_issuing]
    get_invoice_issuing.short_description = "开票单位"

    def get_receive_date(self, obj):
        return obj.invoice_id.receive_date
    get_receive_date.short_description = "到账日期"

    # def get_receivables(self, obj):
    #     return obj.invoice_id.receivables
    # get_receivables.short_description = "应收金额"

    def get_address_name(self, obj):
        return obj.invoice_id.address_name
    get_address_name.short_description = "收件人姓名"

    def get_address_phone(self, obj):
        return obj.invoice_id.address_phone
    get_address_phone.short_description = "收件人电话"

    def get_send_address(self, obj):
        return obj.invoice_id.send_address
    get_send_address.short_description = "收件人地址"

    def get_readonly_fields(self, request, obj=None):
        if hasattr(obj, 'invoice_approval_status'):
            if obj.invoice_approval_status is not None:
                self.readonly_fields = self.invoice_info + \
                                       ('invoice_id', 'invoice_approval_status',)
        if hasattr(obj, 'send_flag'):
            if obj.send_flag:
                self.readonly_fields = self.invoice_info + \
                                       ('invoice_approval_status',) + \
                                       self.send_invoice_info
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        send_invoice = SendInvoices.objects.filter(pk=object_id)
        self.get_readonly_fields(request, obj=send_invoice)
        return super(SendInvoiceAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    # def get_changeform_initial_data(self, request):
    #     initial = super(SendInvoiceAdmin, self).get_changeform_initial_data(request)
    #     initial['fill_name'] = request.user
    #     return initial

    def save_model(self, request, obj, form, change):
        if change:
            obj.fill_name = request.user
        super(SendInvoiceAdmin, self).save_model(request, obj, form, change)
