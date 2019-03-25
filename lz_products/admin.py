import os
import subprocess
import zipfile

from django.contrib import admin
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils import timezone

from import_export.admin import ImportExportModelAdmin

from bms_colowell.settings import MEDIA_ROOT
from lz_products.resources import LzProductsResource
from lz_products.models import BatchDownloadRecords


class LzProductsAdmin(ImportExportModelAdmin):
    """Admin for LZ products."""
    
    actions = ["create_download_record"]
    fields = (
        'sample_code', 'barcode', 'risk_state', 'received_date', 'test_date',
        'report_date', 'pdf_upload',
    )
    list_display = (
        'sample_code', 'barcode', 'risk_state', 'received_date', 'test_date',
        'report_date', 'report_download',
    )
    list_display_links = ('barcode', )
    list_per_page = 30
    resource_class = LzProductsResource
    save_as_continue = False
    search_fields = ('sample_code', 'barcode', )
    
    @staticmethod
    def get_report(request, obj, token):
        """Method to generate pdf file."""
        
        # Generate pdf file by execute command line using wkhtmltopdf
        barcode = obj.barcode
        kwargs = {
            "barcode": barcode, "token": token, "user_id": request.user.id,
        }
        url = reverse("lz_products:lz_report", kwargs=kwargs)
        uri = "{}://{}{}".format(request.scheme, request.get_host(), url)

        sample_code, risk_state = obj.sample_code, obj.risk_state
        output = "lz_reports/{}{}.pdf".format(sample_code, risk_state)
        output_absolute_path = os.path.join(MEDIA_ROOT, output)
        command = [
            "wkhtmltopdf", "-q", "--disable-smart-shrinking",
            "-L", "0mm", "-R", "0mm", "-T", "0mm", "-B", "0mm"
        ]
        command.extend([uri, output_absolute_path])
        get_pdf = subprocess.Popen(command)
        get_pdf.wait()
        
        # save pdf report to the corresponding model instance
        obj.pdf_upload = output
        obj.save()
    
    def create_download_record(self, request, queryset):
        """Actions to create download record."""
        
        token = default_token_generator.make_token(request.user)
        
        # Record each time of download
        serial_number = timezone.now().strftime("%Y%m%d%H%M%S")
        record = BatchDownloadRecords.objects.create(
            serial_number=serial_number
        )
        
        # Make sure the existence of pdf files for the first, and then put
        # these into the zip file, a collection for selected sample code.
        base_path = os.path.join(MEDIA_ROOT, 'lz_reports')
        output_path = os.path.join(MEDIA_ROOT, 'zipped_files')
        zip_name = os.path.join(output_path, '{}.zip'.format(serial_number))
        
        with zipfile.ZipFile(zip_name, mode='w') as zip_fh:
            for obj in queryset:
                self.get_report(request, obj, token)
                sample_code, risk_state = obj.sample_code, obj.risk_state
                report_name = "{}{}.pdf".format(sample_code, risk_state)
                absolute_path = os.path.join(base_path, report_name)
                zip_fh.write(absolute_path, report_name)
        
        # Store the zipped report into records, but the download uri keeps
        # effective within 7 days(depends on the token).
        kwargs = {
            "serial_number": serial_number, "token": token,
            "user_id": request.user.id,
        }
        url = reverse("lz_products:batch_download", kwargs=kwargs)
        uri = "{}://{}{}".format(request.scheme, request.get_host(), url)
        record.zipped_file = "zipped_files/{}.zip".format(serial_number)
        record.file_counts = queryset.count()
        record.download_by = request.user
        record.download_uri = uri
        record.save()
        
        # Message user a download link
        message = '文件已打包，点击<a href="{}"><b>下载</b></a>'.format(uri)
        self.message_user(request, message)
    
    create_download_record.short_description = "批量操作-【生成&打包】报告"
    
    def batch_generate_report(self, request, queryset):
        """Actions to batch generate report."""
        
        token = default_token_generator.make_token(request.user)
        for obj in queryset:
            self.get_report(request, obj, token)
        self.message_user(request, "已批量生成选定报告")

    batch_generate_report.short_description = "批量操作-【生成】报告"


class BatchDownloadRecordsAdmin(admin.ModelAdmin):
    """Admin for batch download records."""
    
    fields = (
        'serial_number', 'download_by', 'created_at', 'file_counts',
        'zipped_file', 'download_uri'
    )
    list_display = (
        'serial_number', 'download_by', 'created_at', 'file_counts',
        'download_uri',
    )
    list_display_links = ('serial_number', )
    list_per_page = 30
    readonly_fields = (
        'serial_number', 'download_by', 'created_at', 'file_counts',
        'zipped_file', 'download_uri'
    )
    save_as_continue = False
