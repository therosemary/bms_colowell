from import_export import resources
from import_export.fields import Field
from import_export.widgets import IntegerWidget, DecimalWidget, \
    ForeignKeyWidget, DateWidget
from projects.models import ContractsInfo, InvoiceInfo, BoxApplications


class ContractInfoResources(resources.ModelResource):
    """合同信息导入导出resources"""

    contract_id = Field(
        column_name="合同编号", attribute='contract_id'
    )
    contract_number = Field(
        column_name="合同号", attribute='contract_number'
    )
    client = Field(
        column_name="客户", attribute='client', default=None
    )
    staff_name = Field(
        column_name="业务员", attribute='staff_name', default=None
    )
    box_price = Field(
        column_name="盒子单价", attribute='box_price'
    )
    detection_price = Field(
        column_name="检测单价", attribute='detection_price'
    )
    full_set_price = Field(
        column_name="全套价格", attribute='full_set_price', default=None
    )
    contract_money = Field(
        column_name="合同金额", attribute='contract_money'
    )
    count_invoice_value = Field(
        column_name="已开票额", attribute='count_invoice_value', default=None
    )
    receive_invoice_value = Field(
        column_name="已到账额", attribute='receive_invoice_value', default=None
    )
    send_date = Field(
        column_name="合同寄出时间", attribute='send_date', default=None
    )
    tracking_number = Field(
        column_name="邮寄单号", attribute='tracking_number'
    )
    send_back_date = Field(
        column_name="合同寄回时间", attribute='send_back_date', default=None
    )
    shipping_status = Field(
        column_name="发货状态", attribute='shipping_status'
    )
    contract_type = Field(
        column_name="合同类型", attribute='contract_type'
    )
    end_status = Field(
        column_name="是否完结", attribute='end_status'
    )

    class Meta:
        model = ContractsInfo
        fields = (
            'contract_id', 'contract_number', 'client', 'staff_name',
            'box_price', 'detection_price', 'full_set_price', 'contract_money',
            'count_invoice_value', 'receive_invoice_value', 'send_date',
            'tracking_number', 'send_back_date', 'shipping_status',
            'contract_type', 'end_status'
        )
        export_order = (
            'contract_id', 'contract_number', 'client', 'staff_name',
            'box_price', 'detection_price', 'full_set_price', 'contract_money',
            'count_invoice_value', 'receive_invoice_value', 'send_date',
            'tracking_number', 'send_back_date', 'shipping_status',
            'contract_type', 'end_status'
        )
        import_id_fields = ['contract_id']
        skip_unchanged = True

    def get_export_headers(self):
        export_headers = [u'合同编号', u'合同号', u'客户', u'业务员', u'盒子单价',
                          u'检测单价', u'全套价格', u'合同金额', u'已开票额',
                          u'已到账额', u'合同寄出时间', u'邮件单号', u'合同寄回时间',
                          u'发货状态', u'合同类型', u'是否完结']
        return export_headers

    def dehydrate_full_set_price(self, contractinfo):
        """计算全套价格"""
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
    """发票信息导入导出resources"""

    invoice_id = Field(
        column_name="发票编号", attribute='invoice_id'
    )
    contract_number = Field(
        column_name="合同号", attribute='contract_id__contract_number',
    )
    cost_type = Field(
        column_name="发票类型", attribute='cost_type'
    )
    invoice_title = Field(
        column_name="发票抬头", attribute='invoice_title'
    )
    tariff_item = Field(
        column_name="税号", attribute='tariff_item'
    )
    invoice_value = Field(
        column_name="开票金额", attribute='invoice_value'
    )
    tax_rate = Field(
        column_name="税率", attribute='tax_rate'
    )
    invoice_issuing = Field(
        column_name="开票单位", attribute='invoice_issuing'
    )
    receive_date = Field(
        column_name="到账日期", attribute='receive_date'
    )
    receivables = Field(
        column_name="应收金额", attribute='receivables'
    )
    address_name = Field(
        column_name="收件人姓名", attribute='address_name'
    )
    address_phone = Field(
        column_name="收件人号码", attribute='address_phone'
    )
    send_address = Field(
        column_name="寄送地址", attribute='send_address'
    )
    apply_name = Field(
        column_name="申请人", attribute='apply_name'
    )
    remark = Field(
        column_name="备注", attribute='remark'
    )
    flag = Field(
        column_name="是否提交", attribute='flag'
    )
    approval_status = Field(
        column_name="审批状态", attribute='sendinvoices__invoice_approval_status'
    )

    class Meta:
        model = InvoiceInfo
        fields = (
            'invoice_id', 'contract_number', 'cost_type', 'invoice_title',
            'tariff_item', 'invoice_value', 'tax_rate', 'invoice_issuing',
            'receive_date', 'receivables', 'address_name', 'address_phone',
            'send_address', 'apply_name', 'remark', 'flag', 'approval_status'
        )
        export_order = fields
        skip_unchanged = True
        import_id_fields = ['invoice_id']

    def get_export_headers(self):
        export_headers = [u'发票编号', u'合同号', u'发票类型', u'发票抬头', u'税号',
                          u'开票金额', u'税率', u'开票单位', u'到账日期', u'应收金额',
                          u'收件人姓名', u'收件人号码', u'寄送地址', u'申请人',
                          u'备注', '是否提交', u'审批状态']
        return export_headers


class BoxApplicationsResources(resources.ModelResource):
    """盒子申请信息导入导出"""

    application_id = Field(
        column_name="申请编号", attribute='application_id', default=None
    )
    # TODO: 合同号导出时，无法获取
    contract_id = Field(
        column_name="合同号", attribute='contract_id',
        widget=ForeignKeyWidget(ContractsInfo, 'contract_number'), default=None
    )
    amount = Field(
        column_name="申请数量", attribute='amount', widget=IntegerWidget()
    )
    classification = Field(
        column_name="申请类别", attribute='classification'
    )
    address_name = Field(
        column_name="收件人姓名", attribute='address_name'
    )
    address_phone = Field(
        column_name="收件人号码", attribute='address_phone'
    )
    send_address = Field(
        column_name="邮寄地址", attribute='send_address'
    )
    box_price = Field(
        column_name="盒子单价", attribute='box_price', default=None
    )
    detection_price = Field(
        column_name="检测单价", attribute='detection_price', default=None
    )
    use = Field(
        column_name="用途", attribute='use'
    )
    proposer = Field(
        column_name="申请人", attribute='proposer', default=None
    )
    submit_time = Field(
        column_name="提交时间", attribute='submit_time', widget=DateWidget(
            '%Y-%m-%d')
    )
    approval_status = Field(
        column_name="审批状态", attribute='approval_status'
    )
    box_submit_flag = Field(
        column_name="是否提交", attribute='box_submit_flag'
    )

    class Meta:
        model = BoxApplications
        fields = (
            'application_id', 'contract_id', 'amount', 'classification',
            'address_name', 'address_phone', 'send_address', 'box_price',
            'detection_price', 'use', 'proposer', 'submit_time',
            'approval_status', 'box_submit_flag'
        )
        export_order = (
            'application_id', 'contract_id', 'amount', 'classification',
            'address_name', 'address_phone', 'send_address', 'box_price',
            'detection_price', 'use', 'proposer', 'submit_time',
            'approval_status', 'box_submit_flag'
        )
        skip_unchanged = True
        import_id_fields = ['application_id']

    def get_export_headers(self):
        export_headers = [u'申请编号', u'合同号', u'申请数量', u'申请类别',
                          u'收件人姓名', u'收件人号码', u'邮寄地址', u'盒子单价',
                          u'检测单价', u'用途', u'申请人', u'提交时间', u'审批状态',
                          u'是否提交']
        return export_headers
