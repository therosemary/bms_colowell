from django.db.models import Sum

from import_export.widgets import DateWidget, ForeignKeyWidget
from import_export.fields import Field
from import_export import resources

from projects.models import ContractsInfo
from partners.models import Partners
from bs_invoices.models import BusinessRecord


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
        column_name="客户", attribute='client', default=None,
        widget=ForeignKeyWidget(Partners, 'name')
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
        column_name="业务员", attribute='staff_name__username', default=None
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

    def dehydrate_full_set_price(self, contractinfo):
        """计算全套价格"""
        if contractinfo.box_price is not None and contractinfo.detection_price \
                is not None:
            full_set_price = contractinfo.box_price + contractinfo.detection_price
        else:
            full_set_price = None
        return full_set_price

    def dehydrate_receive_invoice_value(self, contractinfo):
        """获取已到账总金额"""
        receive_value = 0
        bussiness_record = BusinessRecord.objects.filter(
            contract_number=contractinfo.id)
        if len(bussiness_record):
            for record_data in bussiness_record:
                payment_data = record_data.payment_set.all()
                pay = payment_data.aggregate(value=Sum('receive_value'))
                pay_amount = pay.get('value', 0)
                receive_value += pay_amount
        return receive_value
