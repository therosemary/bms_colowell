from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateWidget
from intentions.models import Intentions


class IntentionSource(resources.ModelResource):
    """意向池导入导出resources"""

    id = Field(
        column_name="编号", attribute='id', default=None
    )
    salesman = Field(
        column_name="销售", attribute='salesman', default=None
    )
    intention_client = Field(
        column_name="意向名称", attribute='intention_client'
    )
    contact_name = Field(
        column_name="联系人姓名", attribute='contact_name'
    )
    contact_number = Field(
        column_name="电话(或微信)", attribute='contact_number'
    )
    follow_situations = Field(
        column_name="跟进情况", attribute='follow_situations'
    )
    material_situations = Field(
        column_name="物料情况", attribute='material_situations'
    )
    other_situations = Field(
        column_name="其他情况", attribute='other_situations'
    )
    remark = Field(
        column_name="备注", attribute='remark'
    )
    fill_date = Field(
        column_name="填写日期", attribute='fill_date', default=None,
        widget=DateWidget(format='%Y-%m-%d')
    )

    class Meta:
        model = Intentions
        fields = (
            'id', 'salesman', 'intention_client', 'contact_name',
            'contact_number', 'follow_situations', 'material_situations',
            'other_situations', 'remark', 'fill_date'
        )
        export_order = fields
        skip_unchanged = True
        import_id_fields = ['id']

    def get_export_headers(self):
        export_headers = [u'编号', u'销售', u'意向客户', u'合同号', u'电话(或微信)',
                          u'跟进情况', u'物料情况', u'其他情况', u'备注', u'填写日期']
        return export_headers
