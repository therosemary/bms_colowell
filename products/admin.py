from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from products.resources import ProductsResource


class ProductsAdmin(ImportExportModelAdmin):
    resource_class = ProductsResource
    fields = (
        "barcode", "is_approved", "is_sold_out", "is_bound", "add_date",
        "sold_date", "sold_to", "sold_way", "operator",
    )
    list_per_page = 30
    list_display = (
        "barcode", "is_approved", "is_sold_out", "is_bound", "add_date",
        "sold_date", "sold_to", "sold_way", "operator",
    )
    list_display_links = ('barcode', )
    list_filter = ("is_bound", "is_sold_out", "is_approved")
    save_as_continue = False
    search_fields = ("barcode", "operator", )
