from partners.models import Partners
from import_export import resources
from import_export.fields import Field

class PartnersResources(resources.ModelResource):
    """代理商信息导入导出resources"""

    bms_user = Field(
        column_name="业务员", attribute='bms_user', default=None
    )
    name = Field(
        column_name="合作方名称", attribute='name',
    )
    code = Field(
        column_name="合同编号", attribute='code'
    )
    reporting_period = Field(
        column_name="出报告周期", attribute='reporting_period'
    )
    mode = Field(
        column_name="性质", attribute='mode'
    )
    region = Field(
        column_name="区域", attribute='region'
    )
    created_at = Field(
        column_name="始建于", attribute='created_id'
    )
    altered_at = Field(
        column_name="修改于", attribute='altered_at'
    )
    materials = Field(
        column_name="物料支持", attribute='materials'
    )
    sponsorship = Field(
        column_name="会议赞助支持", attribute='sponsorship'
    )
    activities = Field(
        column_name="策划活动支持", attribute='activities'
    )
    propaganda = Field(
        column_name="宣讲", attribute='propaganda'
    )
    note = Field(
        column_name="备注信息", attribute='note'
    )

    class Meta:
        model = Partners
        fields = (
            'bms_user', 'name', 'code', 'reporting_period', 'mode', 'region',
            'created_at', 'altered_at', 'materials', 'sponsorship',
            'activities', 'propaganda', 'note',
        )
        export_order = fields
        skip_unchanged = True
        import_id_fields = ['code']

    def get_export_headers(self):
        export_headers = [u'业务员', u'合作方名称', u'合同编号', u'出报告周期',
                          u'性质', u'区域', u'始建于', u'修改于', u'物料支持',
                          u'会议赞助支持', u'策划活动支持', u'宣讲', u'备注信息']
        return export_headers
