from products.models import Products
from import_export import resources, fields


class ProductsResource(resources.ModelResource):
    """The import_export resource class for model Products"""
    barcode = fields.Field(attribute="barcode", column_name="条形码")

    class Meta:
        model = Products
        import_id_fields = ('barcode',)
        skip_unchanged = True
        fields = ("barcode",)
        export_order = ("barcode",)

    def get_export_headers(self):
        return ["条形码",]
