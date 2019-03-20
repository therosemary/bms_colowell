import os
import subprocess
import zipfile

from django.contrib.auth.tokens import default_token_generator
from django.http import StreamingHttpResponse
from django.urls import path, reverse

from import_export.admin import ImportExportModelAdmin
from lz_products.resources import LzProductsResource
from bms_colowell.settings import MEDIA_ROOT


def file_iterator(file_name, chunk_size=512):
    with open(file_name, 'rb') as file_stream:
        while True:
            chunk = file_stream.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break


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
        barcode = obj.barcode
        kwargs = {
            "barcode": barcode, "token": token, "user_id": request.user.id,
        }
        url = reverse("lz_products:lz_report", kwargs=kwargs)
        input = "{}://{}{}".format(request.scheme, request.get_host(), url)

        sample_code, risk_state = obj.sample_code, obj.risk_state
        output = "lz_reports/{}{}.pdf".format(sample_code, risk_state)
        output_absolute_path = os.path.join(MEDIA_ROOT, output)
        command = [
            "wkhtmltopdf", "-q", "--disable-smart-shrinking",
            "-L", "0mm", "-R", "0mm", "-T", "0mm", "-B", "0mm"
        ]
        command.extend([input, output_absolute_path])
        get_pdf = subprocess.Popen(command)
        get_pdf.wait()
    
        # save pdf report to the corresponding model instance
        obj.pdf_upload = output
        obj.save()

    def batch_download_report(self, request, queryset):
        """Actions to batch download a couple of reports."""
        
        base_path = os.path.join(MEDIA_ROOT, 'lz_reports')
        zip_name = os.path.join(base_path, 'batch.zip')
        token = default_token_generator.make_token(request.user)
        
        # Generate pdf file for the first, and then the zip file, a collection
        # for selected sample code.
        with zipfile.ZipFile(zip_name, mode='w') as zip_fh:
            for obj in queryset:
                self.get_report(request, obj, token)
                sample_code, risk_state = obj.sample_code, obj.risk_state
                report_name = "{}{}.pdf".format(sample_code, risk_state)
                absolute_path = os.path.join(base_path, report_name)
                zip_fh.write(absolute_path, report_name)
        
        # Depart the zip file into file stream, thus to StreamingHttpResponse
        file, content_type = file_iterator(zip_name), 'application/zip'
        response = StreamingHttpResponse(file, content_type=content_type)
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
            "reports.zip"
        )
        return response
    batch_download_report.short_description = "批量生成并下载PDF报告"
