from import_export import resources
from import_export.fields import Field
from intentions.models import Intentions


class IntentionSource(resources.ModelResource):
    """意向池导入导出resources"""

    intention_id = Field(
        column_name="编号", attribute='intention_id'
    )
    intention_client = Field(
        column_name="意向客户", attribute='intention_client'
    )
    contact_number = Field(
        column_name="联系电话", attribute='contact_number'
    )
    items = Field(
        column_name="事项", attribute='items'
    )
    fill_date = Field(
        column_name="填写日期", attribute='fill_date'
    )
    fill_name = Field(
        column_name="填写人", attribute='fill_name', default=None
    )
    submit_flag = Field(
        column_name="是否提交", attribute='submit_flag'
    )

    class Meta:
        model = Intentions
        fields = (
            'intention_id', 'intention_client', 'contact_number', 'items',
            'fill_date', 'fill_name', 'submit_flag'
        )
        export_order = (
            'intention_id', 'intention_client', 'contact_number', 'items',
            'fill_date', 'fill_name', 'submit_flag'
        )
        skip_unchanged = True
        import_id_fields = ['intention_id']

    def get_export_headers(self):
        export_headers = [u'编号', u'意向客户', u'联系电话', u'事项', u'填写日期',
                          '填写人', '是否提交']
        return export_headers
