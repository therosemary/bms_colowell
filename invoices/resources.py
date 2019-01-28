from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, DateWidget
from projects.models import InvoiceInfo
from invoices.models import SendInvoices


class SendInvoiceResources(resources.ModelResource):
    """发票详细信息rsources"""

    id = Field(
        column_name='编号', attribute='id', default=None
    )
    invoice_id = Field(
        column_name="发票编号", attribute='invoice_id', default=None,
        widget=ForeignKeyWidget(InvoiceInfo, 'invoice_id')
    )
    invoice_number = Field(
        column_name="发票号码", attribute='invoice_number'
    )
    contract_number = Field(
        column_name="合同号", attribute='contract_number', default=None
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
        column_name="开票单位", attribute='invoice_id__invoice_issuing',
        readonly=True,
    )
    receive_date = Field(
        column_name="到款日期", attribute='invoice_id__receive_date', default=None,
        widget=DateWidget(format='%Y-%m-%d'),
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
    invoice_approval_status = Field(
        column_name="审批状态", attribute='invoice_approval_status'
    )
    billing_date = Field(
        column_name="开票日期", attribute='billing_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None,
    )
    invoice_send_date = Field(
        column_name="发票寄出时间", attribute='invoice_send_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None,
    )
    tracking_number = Field(
        column_name="快递单号", attribute='tracking_number'
    )
    invoice_flag = Field(
        column_name="到款标志", attribute='invoice_flag'
    )
    sender = Field(
        column_name="寄件人", attribute='sender'
    )
    send_flag = Field(
        column_name="是否提交", attribute='send_flag'
    )

    class Meta:
        model = SendInvoices
        fields = (
            'id', 'invoice_id', 'invoice_number', 'contract_number',
            'invoice_title', 'tariff_item', 'invoice_value', 'tax_rate',
            'invoice_issuing', 'receive_date', 'receivables', 'apply_name',
            'invoice_approval_status', 'address_name', 'address_phone',
            'send_address', 'billing_date', 'invoice_send_date',
            'tracking_number', 'invoice_flag', 'sender', 'send_flag',
        )
        export_order = (
            'id', 'invoice_id', 'invoice_number', 'contract_number',
            'invoice_title', 'tariff_item', 'invoice_value', 'tax_rate',
            'invoice_issuing', 'receive_date', 'receivables', 'apply_name',
            'invoice_approval_status', 'address_name', 'address_phone',
            'send_address', 'billing_date', 'invoice_send_date',
            'tracking_number', 'invoice_flag', 'sender', 'send_flag',
        )
        skip_unchanged = True

    def get_export_headers(self):
        export_headers = [u'编号', u'发票编号', u'发票号码', u'合同号', u'发票抬头',
                          u'税号', u'开票金额', u'税率', u'开票单位', u'到款日期',
                          u'应收金额', u'申请人', u'审批状态', u'收件人姓名',
                          u'收件人电话', u'收件人地址', u'开票日期', u'发票寄出时间',
                          u'快递单号', u'到款标志', u'寄件人', u'是否提交']
        return export_headers

    def dehydrate_contract_number(self, sendinvoices):
        invoice_data = InvoiceInfo.objects.get(invoice_id=sendinvoices.invoice_id)
        return invoice_data.contract_id.contract_number

    def dehydrate_invoice_issuing(self, sendinvoices):
        issuing_entities = {'shry': '上海锐翌', 'hzth': '杭州拓宏', 'hzry': '杭州锐翌'}
        return issuing_entities[sendinvoices.invoice_id.invoice_issuing]
