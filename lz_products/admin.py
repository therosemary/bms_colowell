import os
import subprocess
import zipfile

from django.contrib import admin
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.db.models.fields.related import ForeignKey
from django.http import HttpResponseRedirect
from django.template.response import HttpResponse, TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

from import_export.admin import ImportExportModelAdmin
from import_export.forms import ConfirmImportForm

from bms_colowell.settings import MEDIA_ROOT
from lz_products.resources import LzProductsResource
from lz_products.models import LzProducts, BatchDownloadRecords


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
        _url = reverse("lz_products:lz_report", kwargs=kwargs)
        _uri = "{}://{}{}".format(request.scheme, request.get_host(), _url)

        sample_code, risk_state = obj.sample_code, obj.risk_state
        output = "lz_reports/{}{}.pdf".format(sample_code, risk_state)
        output_absolute_path = os.path.join(MEDIA_ROOT, output)
        command = [
            "wkhtmltopdf", "-q", "--disable-smart-shrinking",
            "-L", "0mm", "-R", "0mm", "-T", "0mm", "-B", "0mm"
        ]
        command.extend([_uri, output_absolute_path])
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
    
    def append_fk_col(self, request, dataset):
        """Method to append fk column(foreignkey) into the dataset."""
    
        # The first step is to get all the foreignkey fields
        current_model_fk = []
        for field in self.model._meta.local_fields:
            if isinstance(field, ForeignKey):
                current_model_fk.append(field)
    
        # Then to check whether such fk field are stored into the request
        # session, if it is true, append a new column with the same length
        # as the dataset to the dataset.
        for fk in current_model_fk:
            if fk.attname in request.session.keys():
                fk_val = request.session.get(fk.attname, "")
                fk_col = [fk_val for _t in range(len(dataset))]
                dataset.append_col(fk_col, header=fk.verbose_name)
    
    @method_decorator(require_POST)
    def process_import(self, request, *args, **kwargs):
        """Perform the actual inline import action (after the user has
        confirmed the import)"""
        
        if not self.has_import_permission(request):
            raise PermissionDenied
        
        confirm_form = ConfirmImportForm(request.POST)
        if confirm_form.is_valid():
            import_formats = self.get_import_formats()
            input_format = import_formats[
                int(confirm_form.cleaned_data['input_format'])
            ]()
            tmp_storage = self.get_tmp_storage_class()(
                name=confirm_form.cleaned_data['import_file_name'])
            data = tmp_storage.read(input_format.get_read_mode())
            if not input_format.is_binary() and self.from_encoding:
                data = force_text(data, self.from_encoding)
            dataset = input_format.create_dataset(data)

            # Only if a session key of "redirect_to" is set, the fk column
            # will be appended to the dataset
            if "redirect_to" in request.session.keys():
                self.append_fk_col(request, dataset)

            result = self.process_dataset(dataset, confirm_form, request,
                                          *args, **kwargs)
            
            tmp_storage.remove()
            
            return self.process_result(result, request)

    def process_result(self, result, request):
        # Only if a session key of "redirect_to" is set, the fk column
        # will be redirect to inline model
        if "redirect_to" in request.session.keys():
            return HttpResponseRedirect(request.session.get("redirect_to"))
        return super().process_result(result, request)
    
    def import_action(self, request, *args, **kwargs):
        """
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        """
        if not self.has_import_permission(request):
            raise PermissionDenied
        
        resource = self.get_import_resource_class()(
            **self.get_import_resource_kwargs(request, *args, **kwargs))
        
        context = self.get_import_context_data()
        
        import_formats = self.get_import_formats()
        form_type = self.get_import_form()
        form = form_type(import_formats,
                         request.POST or None,
                         request.FILES or None)
        
        if request.POST and form.is_valid():
            input_format = import_formats[
                int(form.cleaned_data['input_format'])
            ]()
            import_file = form.cleaned_data['import_file']
            
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            tmp_storage = self.write_to_tmp_storage(import_file, input_format)
            
            # then read the file, using the proper format-specific mode
            # warning, big files may exceed memory
            try:
                data = tmp_storage.read(input_format.get_read_mode())
                if not input_format.is_binary() and self.from_encoding:
                    data = force_text(data, self.from_encoding)
                
                dataset = input_format.create_dataset(data)
                
            except UnicodeDecodeError as e:
                return HttpResponse(u"<h1>导入文件编码错误: %s</h1>" % e)
            except Exception as e:
                return HttpResponse(
                    u"读取文件时<h1>%s 异常发生: %s</h1>" % (
                        type(e).__name__, import_file.name))
            
            # Only if a session key of "redirect_to" is set, the fk column
            # will be appended to the dataset
            if "redirect_to" in request.session.keys():
                self.append_fk_col(request, dataset)

            result = resource.import_data(
                dataset, dry_run=True, raise_errors=False,
                file_name=import_file.name, user=request.user
            )
            
            context['result'] = result
            
            if not result.has_errors() and not result.has_validation_errors():
                context['confirm_form'] = ConfirmImportForm(initial={
                    'import_file_name': tmp_storage.name,
                    'original_file_name': import_file.name,
                    'input_format': form.cleaned_data['input_format'],
                })
        
        context.update(self.admin_site.each_context(request))
        
        context['title'] = _("Import")
        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in
                             resource.get_user_visible_fields()]
        
        request.current_app = self.admin_site.name
        return TemplateResponse(request, [self.import_template_name], context)


class LzProductsInline(admin.TabularInline):
    model = LzProducts
    extra = 0
    fields = (
        'sample_code', 'barcode', 'risk_state', 'pdf_upload',
    )
    readonly_fields = (
        'sample_code', 'barcode', 'risk_state', 'pdf_upload',
    )
    show_change_link = False


class BatchesAdmin(admin.ModelAdmin):
    fields = ('batch_code', 'create_at',)
    list_display = ('batch_code', 'create_at',)
    list_display_links = ('batch_code', )
    list_per_page = 30
    inlines = [LzProductsInline]
    
    @staticmethod
    def _get_model_info(model):
        return model._meta.app_label, model._meta.model_name
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Reconstruct the change view in order to pass inline import data for
        current model admin."""
        
        extra_context = extra_context or {}
        
        # Get all inline model and prepare context for each of them.
        inline_import_urls = []
        for inline_model in self.inlines:
            model_info = self._get_model_info(inline_model.model)
            redirect_url = reverse("admin:{}_{}_import".format(*model_info))
            verbose_name = inline_model.model._meta.verbose_name

            model_info_dict = {"verbose_name": verbose_name,
                               "redirect_url": redirect_url, }
            inline_import_urls.append(model_info_dict)
        
        # Besides, we need to store a redirect url in order to redirect back to
        # current changelist view after the import.
        current_model_info = self._get_model_info(self.model)
        whole_url_name = "admin:{}_{}_changelist".format(*current_model_info)
        redirect_to = reverse(whole_url_name)
        
        # The last step is to store the primary key of the model into
        # request.session, bring this state to the import view of inline model
        pk_name = "{}_id".format(self.model._meta.pk.attname)
        request.session[pk_name] = object_id
        request.session["redirect_to"] = redirect_to
        
        # refresh the context
        extra_context["inline_import_urls"] = inline_import_urls
        return super().change_view(request, object_id,
                                   extra_context=extra_context)


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
