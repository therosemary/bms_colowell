from django.contrib import admin
# from projects.models import InvoiceInfo
# from django.utils.html import format_html
from .models import SendInvoices


class SendInvoiceAdmin(admin.ModelAdmin):
    """发票寄送信息管理
       注：每条记录在发票申请提交后自动被创建
    """
    fields = (
        'invoice_id', 'invoice_number', 'billing_date', 'send_date',
        'tracking_number', 'ele_invoice', 'invoice_flag', 'sender', 'flag'
    )
    list_display = (
        'invoice_id', 'invoice_number', 'billing_date', 'ele_invoice',
        'tracking_number', 'send_date', 'sender', 'invoice_flag',
        'fill_name', 'flag'
    )
    list_per_page = 40
    save_as_continue = False
    readonly_fields = ('invoice_id', 'fill_name')

    def get_readonly_fields(self, request, obj=None):
        # if request.user.is_superuser:
        #     self.readonly_fields = []
        # elif hasattr(obj, 'flag'):
        if hasattr(obj, 'flag'):
            if obj.flag:
                self.readonly_fields = (
                    'invoice_id', 'invoice_number', 'billing_date', 'send_date',
                    'tracking_number', 'ele_invoice', 'invoice_flag', 'sender',
                    'flag'
                )
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        send_invoice = SendInvoices.objects.filter(pk=object_id)
        self.get_readonly_fields(request, obj=send_invoice)
        return super(SendInvoiceAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def save_model(self, request, obj, form, change):
        if change:
            super(SendInvoiceAdmin, self).save_model(request, obj, form, change)
        else:
            obj.fill_name = request.user
            obj.save()
