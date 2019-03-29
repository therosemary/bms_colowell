from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.db.models.fields.related import ForeignKey
from django.template.response import HttpResponse, TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

from import_export.admin import ImportExportModelAdmin
from import_export.forms import ConfirmImportForm

from products.resources import ProductsResource
from products.models import Products


class ProductsInline(admin.TabularInline):
    model = Products
    extra = 0
    fields = (
        "barcode", "is_approved", "is_sold_out", "is_bound", "add_date",
        "sold_date", "sold_to", "sold_way", "operator",
    )
    readonly_fields = (
        "barcode", "is_approved", "is_sold_out", "is_bound", "add_date",
        "sold_date", "sold_to", "sold_way", "operator",
    )
    show_change_link = False


class ProductsAdmin(ImportExportModelAdmin):
    resource_class = ProductsResource
    fields = (
        "barcode", "real_barcode_image", "sold_date", "sold_to", "sold_way",
        "operator", ("is_approved", "is_sold_out", "is_bound"), "serial_number"
    )
    list_per_page = 10
    list_display = (
        "barcode", "real_barcode_image", "is_approved", "is_sold_out", "is_bound",
        "add_date", "sold_date", "sold_to", "sold_way", "operator",
    )
    list_display_links = ('barcode', )
    list_filter = ("is_bound", "is_sold_out", "is_approved")
    readonly_fields = ("real_barcode_image", )
    save_as_continue = False
    search_fields = ("barcode", "operator", )
    
    def real_barcode_image(self, obj):
        return format_html('<img src="{}" alt="{}" height="20%">',
                           obj.barcode_img.url, obj.barcode)
    real_barcode_image.short_description = "条形码"

    def get_session_fk_name(self, request, wanted_fk_name="", column_name=""):
        """Method to get model foreignkey name in session."""
        session_keys = request.session.keys()
    
        # STEP 1. get all of the foreignkey fields of current model.
        current_model_fk = []
        for field in self.model._meta.local_fields:
            if isinstance(field, ForeignKey):
                current_model_fk.append(field)
        
        # STEP 2. to check whether such fk field are stored into the request
        # session, if it is true, return.
        for fk in current_model_fk:
            if fk.attname in session_keys:
                wanted_fk_name = fk.attname
                column_name = fk.verbose_name
        return wanted_fk_name, column_name
    
    def append_fk_col(self, request, dataset):
        """Method to append fk column(foreignkey) into the dataset."""
        session_keys = request.session.keys()
        fk_name, column_name = self.get_session_fk_name(request)
        fk_value = request.session.get(fk_name, "")
        fk_col = [fk_value for _t in range(len(dataset))]
        dataset.append_col(fk_col, header=column_name)
        
        # These useless session data should be deleted after the real import
        # step(dry_run=False).
        if fk_name in session_keys:
            del request.session[fk_name]
            del request.session["redirect_to"]
    
    def append_fk_col_preview(self, request, dataset):
        """Method to append fk column(foreignkey) into the dataset."""
        fk_name, column_name = self.get_session_fk_name(request)
        fk_value = request.session.get(fk_name, "")
        fk_col = [fk_value for _t in range(len(dataset))]
        dataset.append_col(fk_col, header=column_name)

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
                self.append_fk_col_preview(request, dataset)

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


class DeliveriesAdmin(admin.ModelAdmin):
    fields = (
        'serial_number', 'salesman', 'customer', 'is_submit', 'add_date',
    )
    list_display = (
        'serial_number', 'salesman', 'customer', 'is_submit', 'add_date',
    )
    list_display_links = ('serial_number',)
    list_per_page = 30
    inlines = [ProductsInline]

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        initial = context["adminform"].form.initial
        initial['serial_number'] = timezone.now().strftime("%Y%m%d%H%M%S")
        if obj and obj.is_submit:
            context['show_save'] = False
            context['show_delete'] = False
            context['show_save_and_continue'] = False
        return super().render_change_form(
            request, context, add=add, change=change, form_url=form_url,
            obj=obj
        )

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
        
        # TODO: The redirection after import should be handled.
        # current_model_info = self._get_model_info(self.model)
        # whole_url_name = "admin:{}_{}_changelist".format(*current_model_info)
        # redirect_to = reverse(whole_url_name)
        # request.session["redirect_to"] = redirect_to

        # To store the primary key of the model into request.session, bring
        # this state to the import view of inline model
        # TODO: to deal with the session pollution
        pk_name = "{}_id".format(self.model._meta.pk.attname)
        request.session[pk_name] = object_id
        
        # refresh the context
        extra_context["inline_import_urls"] = inline_import_urls
        return super().change_view(request, object_id,
                                   extra_context=extra_context)
