from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from jet.admin import CompactInline
from jet.filters import DateRangeFilter

from bms_colowell.utils import InlineImportExportModelAdmin
from products.resources import ProductsResource
from products.models import Products


class ProductsInline(CompactInline):
    model = Products
    extra = 0
    fields = (
        "barcode", "is_approved", "is_sold_out", "is_bound",
        "sold_date", "sold_to", "sold_way", "operator",
    )
    # readonly_fields = (
    #     "barcode", "is_approved", "is_sold_out", "is_bound", "add_date",
    #     "sold_date", "sold_to", "sold_way", "operator",
    # )
    show_change_link = False


class ProductsAdmin(InlineImportExportModelAdmin):
    resource_class = ProductsResource
    fields = (
        "barcode", "real_barcode_image", "sold_date", "sold_to", "sold_way",
        "operator", ("is_approved", "is_sold_out", "is_bound"), "serial_number"
    )
    list_per_page = 10
    list_display = (
        "barcode", "real_barcode_image", "is_approved", "is_sold_out",
        "is_bound", "add_date", "sold_date", "sold_to", "sold_way", "operator",
    )
    list_display_links = ('barcode', )
    list_filter = (
        "is_bound", "is_sold_out", "is_approved", ("add_date", DateRangeFilter)
    )
    readonly_fields = ("real_barcode_image", )
    save_as_continue = False
    search_fields = ("barcode", "operator", )
    date_hierarchy = "add_date"
    
    def real_barcode_image(self, obj):
        return format_html('<img src="{}" alt="{}" height="20%">',
                           obj.barcode_img.url, obj.barcode)
    real_barcode_image.short_description = "条形码图片"


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
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['serial_number'] = timezone.now().strftime("%Y%m%d%H%M%S")
        return initial
    
    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
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
        request.session["inline_import"] = True
        
        # refresh the context
        extra_context["inline_import_urls"] = inline_import_urls
        return super().change_view(request, object_id,
                                   extra_context=extra_context)
