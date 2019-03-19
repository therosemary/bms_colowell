from lz_products.models import LzProducts
from import_export import resources, fields
from import_export.widgets import DateWidget


class LzProductsResource(resources.ModelResource):
    """The import_export resource class for model Products"""
    barcode = fields.Field(
        attribute="barcode", column_name="常易舒编号",
    )
    sample_code = fields.Field(
        attribute="sample_code", column_name="样本编号",
    )
    risk_state = fields.Field(
        attribute="risk_state", column_name="风险水平",
    )
    received_date = fields.Field(
        attribute="received_date", column_name="收样日期",
        widget=DateWidget(format='%Y-%m-%d')
    )
    test_date = fields.Field(
        attribute="test_date", column_name="检测日期",
        widget=DateWidget(format='%Y-%m-%d')
    )
    report_date = fields.Field(
        attribute="report_date", column_name="报告日期",
        widget=DateWidget(format='%Y-%m-%d')
    )

    class Meta:
        model = LzProducts
        fields = (
            'sample_code', 'barcode', 'risk_state', 'received_date',
            'test_date', 'report_date',
        )
        export_order = (
            'sample_code', 'barcode', 'risk_state', 'received_date',
            'test_date', 'report_date',
        )
        import_id_fields = ['barcode']
        skip_unchanged = True

    def get_export_headers(self):
        export_headers = [
            '样品编号', '常易舒编号', '风险水平', '收样日期', '检测日期', '报告日期',
        ]
        return export_headers
