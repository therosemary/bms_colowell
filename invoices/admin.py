from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from import_export.fields import Field
from projects.models import InvoiceInfo
from invoices.models import SendInvoices
from invoices.forms import SendInvoicesForm


class SendInvoiceResources(resources.ModelResource):
    contract_number = Field(
        column_name="合同号", readonly=True,
    )
    invoice_title = Field(
        column_name="发票抬头", attribute='invoice_id__invoice_title'
    )
    tariff_item = Field(
        column_name="税号", attribute='invoice_id__tariff_item'
    )
    invoice_value = Field(
        column_name="开票金额", attribute='invoice_id__invoice_value'
    )
    tax_rate = Field(
        column_name="税率", attribute='invoice_id__tax_rate'
    )
    invoice_issuing = Field(
        column_name="开票单位",
    )
    receive_date = Field(
        column_name="到款日期", attribute='invoice_id__receive_date'
    )
    receivables = Field(
        column_name="应收金额", attribute='invoice_id__receivables'
    )
    apply_name = Field(
        column_name="申请人", attribute='invoice_id__apply_name'
    )
    address_name = Field(
        column_name="收件人姓名", attribute='invoice_id__address_name'
    )
    address_phone = Field(
        column_name="收件人号码", attribute='invoice_id__address_phone'
    )
    send_address = Field(
        column_name="收件人地址", attribute='invoice_id__send_address'
    )

    class Meta:
        model = SendInvoices
        fields = (
            'invoice_id', 'contract_number', 'invoice_title',
            'tariff_item', 'invoice_value',
            'tax_rate', 'invoice_issuing',
            'receive_date', 'receivables',
            'apply_name', 'invoice_approval_status',
            'address_name', 'address_phone',
            'send_address',
            'billing_date', 'invoice_send_date',
            'tracking_number', 'invoice_flag', 'sender', 'send_flag',
        )
        export_order = (
            'invoice_id', 'contract_number', 'invoice_title',
            'tariff_item', 'invoice_value',
            'tax_rate', 'invoice_issuing',
            'receive_date', 'receivables',
            'apply_name', 'invoice_approval_status',
            'address_name', 'address_phone',
            'send_address',
            'billing_date', 'invoice_send_date',
            'tracking_number', 'invoice_flag', 'sender', 'send_flag',
        )
        skip_unchanged = True

    def get_export_headers(self):
        export_headers = [u'发票编号', u'合同号', u'发票抬头',
                          u'税号', u'开票金额', u'税率',
                          u'开票单位', u'到款日期', u'应收金额', u'申请人', u'审批状态',
                          u'收件人姓名', u'收件人电话', u'收件人地址',
                          u'开票日期',
                          u'发票寄出时间', u'快递单号', u'到款标志', u'寄件人',
                          u'是否提交']
        return export_headers

    def dehydrate_contract_number(self, sendinvoices):
        invoice_data = InvoiceInfo.objects.get(invoice_id=sendinvoices.invoice_id)
        return invoice_data.contract_id.contract_number

    def dehydrate_invoice_issuing(self, sendinvoices):
        issuing_entities = {'shry': '上海锐翌', 'hzth': '杭州拓宏', 'hzry': '杭州锐翌'}
        return issuing_entities[sendinvoices.invoice_id.invoice_issuing]


class SendInvoiceAdmin(ImportExportActionModelAdmin):
    """发票寄送信息管理
       注：每条记录在发票申请提交后自动被创建
    """
    invoice_info = (
        'get_contract_number', 'get_invoice_title', 'get_tariff_item',
        'get_invoice_value', 'get_tax_rate', 'get_invoice_issuing',
        'get_receive_date', 'get_receivables', 'get_address_name',
        'get_address_phone', 'get_send_address', 'get_apply_name',
    )
    send_invoice_info = (
        'invoice_id', 'invoice_number', 'billing_date', 'invoice_send_date',
        'tracking_number', 'ele_invoice', 'invoice_flag', 'sender', 'send_flag',
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
        'invoice_id', 'get_apply_name', 'invoice_number', 'billing_date',
        'ele_invoice', 'tracking_number', 'invoice_send_date', 'sender',
        'invoice_flag', 'fill_name', 'invoice_approval_status', 'send_flag'
    )
    list_per_page = 40
    save_as_continue = False
    date_hierarchy = 'billing_date'
    readonly_fields = ('invoice_id',) + invoice_info
    form = SendInvoicesForm
    list_filter = ('invoice_id__fill_date', 'invoice_id__apply_name')
    resource_class = SendInvoiceResources

    def get_apply_name(self, obj):
        return obj.invoice_id.apply_name
    get_apply_name.short_description = "申请人"

    def get_contract_number(self, obj):
        invoice_data = InvoiceInfo.objects.get(invoice_id=obj.invoice_id)
        return invoice_data.contract_id.contract_number
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

    def get_receivables(self, obj):
        return obj.invoice_id.receivables
    get_receivables.short_description = "应收金额"

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
        # if request.user.is_superuser:
        #     self.readonly_fields = []
        # elif hasattr(obj, 'flag'):

        # 审批状态选定保存后是否提交均不可再修改
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

    def save_model(self, request, obj, form, change):
        if change:
            super(SendInvoiceAdmin, self).save_model(request, obj, form, change)
        else:
            obj.fill_name = request.user
            obj.save()
