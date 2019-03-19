from import_export.admin import ImportExportModelAdmin
from lz_products.resources import LzProductsResource


class LzProductsAdmin(ImportExportModelAdmin):
    fields = (
        'sample_code', 'barcode', 'received_date', 'test_date',
        'report_date', 'pdf_upload',
    )
    list_display = (
        'sample_code', 'barcode', 'received_date', 'test_date',
        'report_date', 'pdf_upload',
    )
    list_per_page = 30
    save_as_continue = False
    resource_class = LzProductsResource
    list_display_links = ('barcode', )
