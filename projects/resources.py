from import_export.widgets import DateWidget
from import_export.fields import Field
from import_export import resources

from projects.models import ContractsInfo


class ContractInfoResources(resources.ModelResource):
    """合同信息导入导出resources"""

    contract_id = Field(
        column_name="编号", attribute='id', default=None
    )
    contract_code = Field(
        column_name="合同编码", attribute='contract_code'
    )
    contract_number = Field(
        column_name="合同号", attribute='contract_number'
    )
    client = Field(
        column_name="客户", attribute='client', default=None
    )
    box_price = Field(
        column_name="盒子单价", attribute='box_price', default=None
    )
    detection_price = Field(
        column_name="检测单价", attribute='detection_price', default=None
    )
    full_set_price = Field(
        column_name="全套价格", attribute='full_set_price', default=None
    )
    contract_money = Field(
        column_name="合同金额", attribute='contract_money', default=None
    )
    # count_invoice_value = Field(
    #     column_name="已开票额", attribute='count_invoice_value', default=None
    # )
    receive_invoice_value = Field(
        column_name="已到账额", attribute='receive_invoice_value', default=None
    )
    send_date = Field(
        column_name="寄出时间", attribute='send_date', default=None,
        widget=DateWidget(format='%Y-%m-%d')
    )
    tracking_number = Field(
        column_name="邮寄单号", attribute='tracking_number'
    )
    send_back_date = Field(
        column_name="寄回时间", attribute='send_back_date', default=None,
        widget=DateWidget(format='%Y-%m-%d')
    )
    contract_type = Field(
        column_name="合同类型", attribute='contract_type'
    )
    start_date = Field(
        column_name="起始时间", attribute='start_date', default=None,
        widget=DateWidget(format='%Y-%m-%d')
    )
    end_date = Field(
        column_name="截止时间", attribute='end_date', default=None,
        widget=DateWidget(format='%Y-%m-%d')
    )
    remark = Field(
        column_name="备注", attribute='remark'
    )
    staff_name = Field(
        column_name="业务员", attribute='staff_name', default=None
    )

    class Meta:
        model = ContractsInfo
        fields = (
            'contract_id', 'contract_code', 'contract_number', 'client',
            'box_price', 'detection_price', 'full_set_price', 'contract_money',
            'receive_invoice_value', 'send_date', 'tracking_number',
            'send_back_date', 'contract_type', 'start_date', 'end_date',
            'remark', 'staff_name',
        )
        export_order = (
            'contract_id', 'contract_code', 'contract_number', 'client',
            'box_price', 'detection_price', 'full_set_price', 'contract_money',
            'receive_invoice_value', 'send_date', 'tracking_number',
            'send_back_date', 'contract_type', 'start_date', 'end_date',
            'remark', 'staff_name',
        )
        import_id_fields = ['contract_id']
        skip_unchanged = True

    def get_export_headers(self):
        export_headers = [u'编号', u'合同编码', u'合同号', u'客户', u'盒子单价',
                          u'检测单价', u'全套价格', u'合同金额', u'已到账额',
                          u'寄出时间', u'邮件单号', u'寄回时间', u'合同类型',
                          u'起始时间', u'截止时间', u'备注', u'业务员', ]
        return export_headers

    def dehydrate_full_set_price(self, contractinfo):
        """计算全套价格"""
        if contractinfo.box_price is not None and contractinfo.detection_price \
                is not None:
            full_set_price = contractinfo.box_price + contractinfo.detection_price
        else:
            full_set_price = None
        return full_set_price

    # def dehydrate_count_invoice_value(self, contractinfo):
    #     """获取已开票总额，包含未审核金额"""
    #     total_value = 0
    #     invoice_datas = InvoiceInfo.objects.filter(
    #         contract_id=contractinfo.contract_id, flag=True
    #     )
    #     if invoice_datas:
    #             for data in invoice_datas:
    #                 if data.sendinvoices.invoice_approval_status:
    #                     total_value += data.invoice_value
    #     return total_value

    def dehydrate_receive_invoice_value(self, contractinfo):
        """获取已到账总金额"""
        receive_value = 0
        payment_datas = PaymentInfo.objects.filter(
            contract_number=contractinfo.id, receive_value__isnull=False)
        if payment_datas is not None:
            for payment in payment_datas:
                receive_value += payment.receive_value
        return receive_value
