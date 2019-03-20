import os
import subprocess

from django.contrib.auth.tokens import default_token_generator
from django.urls import path, reverse

from import_export.admin import ImportExportModelAdmin
from lz_products.resources import LzProductsResource
from bms_colowell.settings import MEDIA_ROOT


class LzProductsAdmin(ImportExportModelAdmin):
    """Admin for LZ products."""
    
    actions = ["batch_download_report"]
    fields = (
        'sample_code', 'barcode', 'risk_state', 'received_date', 'test_date',
        'report_date', 'pdf_upload',
    )
    list_display = (
        'sample_code', 'barcode', 'risk_state', 'received_date', 'test_date',
        'report_date', 'report_download',
    )
    list_per_page = 30
    save_as_continue = False
    resource_class = LzProductsResource
    list_display_links = ('barcode', )

    def get_report(self, request, obj, token):
        """Method to generate pdf file."""
    
        # Generate pdf file by execute command line using wkhtmltopdf
        barcode = obj.product.barcode
        kwargs = {
            "barcode": barcode, "token": token, "user_id": request.user.id,
        }
        url = reverse("lz_products:lz_report", kwargs=kwargs)
        input = "{}://{}{}".format(request.scheme, request.get_host(), url)
        output = os.path.join(MEDIA_ROOT, "lz_reports/{}.pdf".format(barcode))
        command = [
            "wkhtmltopdf", "-q", "--disable-smart-shrinking",
            "-L", "0mm", "-R", "0mm", "-T", "0mm", "-B", "0mm"
        ]
        command.extend([input, output])
        get_pdf = subprocess.Popen(command)
        get_pdf.wait()
    
        # save pdf report to the corresponding model instance
        obj.pdf_upload = "lz_reports/{}.pdf".format(barcode)
        obj.save()

    def batch_download_report(self, request, queryset):
        token = default_token_generator.make_token(request.user)
        for obj in queryset:
            barcode = obj.barcode
            self.get_report(request, obj, token)
            # TODO: to finish the batch download action
            pass
    batch_download_report.short_description = "批量生成并下载PDF报告"
