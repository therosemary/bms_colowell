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
    salesman = Field(
        column_name="业务员", attribute='invoice_id__salesman',
    )
    contract_number = Field(
        column_name="合同号", attribute='contract_number', default=None
    )
    invoice_type = Field(
        column_name="开票类型", attribute='invoice_id__invoice_type'
    )
    invoice_issuing = Field(
        column_name="开票单位", attribute='invoice_id__invoice_issuing',
        readonly=True,
    )
    invoice_title = Field(
        column_name="抬头", attribute='invoice_id__invoice_title'
    )
    tariff_item = Field(
        column_name="税号", attribute='invoice_id__tariff_item'
    )
    send_address = Field(
        column_name="对方地址", attribute='invoice_id__send_address'
    )
    address_phone = Field(
        column_name="号码", attribute='invoice_id__address_phone'
    )
    opening_bank = Field(
        column_name="开户行", attribute='invoice_id__opening_bank'
    )
    bank_account_number = Field(
        column_name="账号", attribute='invoice_id__bank_account_number'
    )
    invoice_value = Field(
        column_name="开票金额", attribute='invoice_id__invoice_value', default=None
    )
    invoice_content = Field(
        column_name="发票内容", attribute='invoice_id__invoice_content'
    )
    remark = Field(
        column_name="备注", attribute='remark'
    )
    apply_name = Field(
        column_name="申请人", attribute='invoice_id__apply_name', default=None
    )
    receive_value = Field(
        column_name="到账金额", attribute='invoice_id__receive_value', default=None
    )
    receive_date = Field(
        column_name="到账时间", attribute='invoice_id__receive_date', default=None,
        widget=DateWidget(format='%Y-%m-%d'),
    )
    invoice_number = Field(
        column_name="发票号码", attribute='invoice_number'
    )
    billing_date = Field(
        column_name="开票日期", attribute='billing_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None,
    )
    invoice_send_date = Field(
        column_name="寄出日期", attribute='invoice_send_date',
        widget=DateWidget(format='%Y-%m-%d'), default=None,
    )
    tracking_number = Field(
        column_name="快递单号", attribute='tracking_number'
    )
    fill_name = Field(
        column_name="填写人", attribute='fill_name', default=None
    )
    send_flag = Field(
        column_name="是否提交", attribute='send_flag'
    )

    class Meta:
        model = SendInvoices
        fields = (
            'id', 'salesman', 'contract_number', 'invoice_type', 'invoice_issuing',
            'invoice_title', 'tariff_item', 'send_address', 'address_phone',
            'opening_bank', 'bank_account_number', 'invoice_value', 'remark',
            'invoice_content', 'apply_name', 'receive_value', 'receive_date',
            'invoice_number', 'billing_date', 'invoice_send_date', 'tracking_number',
            'fill_name', 'send_flag',
        )
        export_order = (
            'id', 'salesman', 'contract_number', 'invoice_type', 'invoice_issuing',
            'invoice_title', 'tariff_item', 'send_address', 'address_phone',
            'opening_bank', 'bank_account_number', 'invoice_value', 'remark',
            'invoice_content', 'apply_name', 'receive_value', 'receive_date',
            'invoice_number', 'billing_date', 'invoice_send_date', 'tracking_number',
            'fill_name', 'send_flag',
        )
        skip_unchanged = True
        import_id_fields = ['id']

    def get_export_headers(self):
        export_headers = [u'编号', u'业务员',  u'合同号', u'开票类型', u'开票单位',
                          u'抬头', u'税号', u'对方地址', u'号码', u'开户行', u'账号',
                          u'开票金额', u'备注', u'发票内容', u'申请人', u'到账金额',
                          u'到账时间', u'发票号码', u'开票日期', u'寄出时间',
                          u'快递单号', u'填写人', u'是否提交']
        return export_headers

    def dehydrate_contract_number(self, sendinvoices):
        invoice_data = InvoiceInfo.objects.get(id=sendinvoices.invoice_id.id)
        return invoice_data.contract_id.contract_number

    def dehydrate_invoice_issuing(self, sendinvoices):
        issuing_entities = {'shry': '上海锐翌', 'hzth': '杭州拓宏', 'hzry': '杭州锐翌',
                            'sdry': '山东锐翌'}
        return issuing_entities[sendinvoices.invoice_id.invoice_issuing]
