from import_export import resources
from import_export.fields import Field
from import_export.widgets import IntegerWidget, DecimalWidget, \
    ForeignKeyWidget, DateWidget
from projects.models import ContractsInfo, InvoiceInfo, BoxApplications


class ContractInfoResources(resources.ModelResource):
    """合同信息导入导出resources"""

    contract_id = Field(
        column_name="编号", attribute='id', default=None
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
            'contract_id', 'contract_number', 'client', 'box_price',
            'detection_price', 'full_set_price', 'contract_money',
            'receive_invoice_value', 'send_date', 'tracking_number',
            'send_back_date', 'contract_type', 'start_date', 'end_date',
            'remark', 'staff_name',
        )
        export_order = (
            'contract_id', 'contract_number', 'client', 'box_price',
            'detection_price', 'full_set_price', 'contract_money',
            'receive_invoice_value', 'send_date', 'tracking_number',
            'send_back_date', 'contract_type', 'start_date', 'end_date',
            'remark', 'staff_name',
        )
        import_id_fields = ['contract_id']
        skip_unchanged = True

    def get_export_headers(self):
        export_headers = [u'编号', u'合同号', u'客户', u'盒子单价', u'检测单价', u'全套价格',
                          u'合同金额', u'已到账额', u'寄出时间', u'邮件单号', u'寄回时间',
                          u'合同类型', u'起始时间', u'截止时间', u'备注', u'业务员', ]
        return export_headers

    def dehydrate_full_set_price(self, contractinfo):
        """计算全套价格"""
        full_set_price = contractinfo.box_price + contractinfo.detection_price
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
        invoice_datas = InvoiceInfo.objects.filter(contract_id=contractinfo.id)
        if invoice_datas:
            for data in invoice_datas:
                if data.sendinvoices.send_flag and data.receive_value is not None:
                    receive_value += data.receive_value
        return receive_value


class InvoiceInfoResources(resources.ModelResource):
    """发票信息导入导出resources"""

    id = Field(
        column_name="编号", attribute='id', default=None
    )
    contract_number = Field(
        column_name="合同号", attribute='contract_id__contract_number',
    )
    salesman = Field(
        column_name="业务员", attribute='salesman',
    )
    invoice_type = Field(
        column_name="开票类型", attribute='invoice_type'
    )
    invoice_issuing = Field(
        column_name="开票单位", attribute='invoice_issuing'
    )
    invoice_title = Field(
        column_name="发票抬头", attribute='invoice_title'
    )
    tariff_item = Field(
        column_name="税号", attribute='tariff_item'
    )
    send_address = Field(
        column_name="对方地址", attribute='send_address'
    )
    address_phone = Field(
        column_name="号码", attribute='address_phone'
    )
    opening_bank = Field(
        column_name="开户行", attribute='opening_bank'
    )
    bank_account_number = Field(
        column_name="账号", attribute='bank_account_number'
    )
    invoice_value = Field(
        column_name="开票金额", attribute='invoice_value', default=None
    )
    invoice_content = Field(
        column_name="开票内容", attribute='invoice_content'
    )
    remark = Field(
        column_name="备注", attribute='remark'
    )
    apply_name = Field(
        column_name="申请人", attribute='apply_name', default=None
    )
    flag = Field(
        column_name="是否提交", attribute='flag'
    )
    receive_value = Field(
        column_name="到账金额", attribute='receive_value', default=None
    )
    receive_date = Field(
        column_name="到账时间", attribute='receive_date',
        widget=DateWidget(format='%Y-%m-%d'),
    )
    fill_date = Field(
        column_name="填写时间", attribute='fill_date',
        widget=DateWidget(format='%Y-%m-%d'),
    )

    class Meta:
        model = InvoiceInfo
        fields = (
            'id', 'contract_number', 'salesman', 'invoice_type',
            'invoice_issuing', 'invoice_title', 'tariff_item',
            'send_address', 'address_phone', 'opening_bank',
            'bank_account_number', 'invoice_value', 'invoice_content', 'remark',
            'apply_name', 'flag', 'receive_value', 'receive_date', 'fill_date',
        )
        export_order = fields
        skip_unchanged = True
        import_id_fields = ['id']

    def get_export_headers(self):
        export_headers = [u'编号', u'合同号', u'业务员', u'开票类型', u'开票单位',
                          u'发票抬头', u'税号', u'对方地址', u'号码', u'开户行',
                          u'账号', u'开票金额', u'开票内容', u'备注', u'申请人',
                          u'是否提交', u'到账金额', u'到账时间', u'填写时间']
        return export_headers


class BoxApplicationsResources(resources.ModelResource):
    """盒子申请信息导入导出"""

    application_id = Field(
        column_name="申请编号", attribute='application_id', default=None
    )
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
