import os

from import_export.admin import ImportExportModelAdmin
from products.resources import ProductsResource
from pystrich.code128 import Code128Encoder
from bms_colowell.settings import MEDIA_ROOT, BARCODE_IMAGE_OPTIONS


class ProductsAdmin(ImportExportModelAdmin):
    resource_class = ProductsResource
    fields = (
        "barcode", "barcode_img", "sold_date", "sold_to", "sold_way",
        "operator", ("is_approved", "is_sold_out", "is_bound"),
    )
    list_per_page = 10
    list_display = (
        "barcode", "is_approved", "is_sold_out", "is_bound", "add_date",
        "sold_date", "sold_to", "sold_way", "operator",
    )
    list_display_links = ('barcode', )
    list_filter = ("is_bound", "is_sold_out", "is_approved")
    save_as_continue = False
    search_fields = ("barcode", "operator", )
    
    @staticmethod
    def generate_barcode_img(obj):
        barcode = obj.barcode
        img_path = os.path.join(MEDIA_ROOT, "products/{}.png".format(barcode))
        encoder = Code128Encoder(barcode, options=BARCODE_IMAGE_OPTIONS)
        encoder.save(img_path)
        obj.barcode_img = "products/{}.png".format(barcode)
        obj.save()
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # TODO: to accomplish the method of generate barcode
        self.generate_barcode_img(obj)
