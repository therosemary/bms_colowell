from products.models import Products
from import_export import resources, fields


class ProductsResource(resources.ModelResource):
    """The import_export resource class for model Products"""
    barcode = fields.Field(
        attribute="barcode", column_name=u"条形码"
    )
    serial_number_id = fields.Field(
        attribute="serial_number_id", column_name=u"发货号"
    )
    
    class Meta:
        model = Products
        import_id_fields = ('barcode', )
        skip_unchanged = True
        fields = ("barcode", "serial_number_id")
        export_order = ("barcode", "serial_number_id")
