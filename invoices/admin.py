import datetime
from django.utils.html import format_html
from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from daterange_filter.filter import DateRangeFilter
# from django.contrib.admin.views.main import ChangeList
from projects.models import InvoiceInfo
from invoices.models import SendInvoices, PaymentInfo
from invoices.forms import SendInvoicesForm
from invoices.resources import SendInvoiceResources, PaymentInfoResource


class PaymentInline(admin.TabularInline):
    model = PaymentInfo.send_invoice.through
    verbose_name = verbose_name_plural = "到账信息"
    extra = 1


class PaymentInfoAdmin(ImportExportActionModelAdmin):
    """到款信息管理"""

    # inlines = [PaymentInline]
    # exclude = ('send_invoice',)
    fields = (
        'receive_value', 'receive_date', 'contract_number', 'send_invoice'
    )
    list_display = (
        'payment_number', 'contract_number', 'receive_value', 'receive_date',
    )
    list_per_page = 30
    save_as_continue = False
    list_display_links = ('payment_number',)
    search_fields = ('payment_number',)
    resource_class = PaymentInfoResource

    def save_model(self, request, obj, form, change):
        if change:
            super(PaymentInfoAdmin, self).save_model(request, obj, form, change)
        else:
            temp = 'RE' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            obj.payment_number = temp
            super(PaymentInfoAdmin, self).save_model(request, obj, form, change)


class SendInvoiceAdmin(ImportExportActionModelAdmin):
    """
    发票寄送信息管理
    注：每条记录在发票申请提交后自动被创建
    """
    # change_list_template = 'admin/invoices/change_list_template_invoices.html'
    inlines = [PaymentInline]
    change_list_template = 'admin/invoices/invoice_change_list.html'
    invoice_info = (
        'get_contract_number', 'get_invoice_type', 'get_invoice_issuing',
        'get_invoice_title', 'get_tariff_item',  'get_send_address',
        'get_address_phone', 'get_opening_bank', 'get_bank_account_number',
        'get_invoice_value', 'get_receive_value', 'get_receive_date',
    )
    send_invoice_info = (
        'invoice_number', 'billing_date', 'invoice_send_date',
        'tracking_number', 'ele_invoice', 'send_flag'
    )
    fieldsets = (
        ('发票申请信息', {
            'fields': invoice_info
        }),
        ('寄送信息填写', {
            'fields': send_invoice_info
        }),
    )
    list_display = (
        'get_salesman', 'get_contract_number', 'billing_date',
        'invoice_number', 'get_invoice_value', 'get_receive_value',
        'receivables', 'get_receive_date', 'get_invoice_title',
        'get_invoice_content', 'tracking_number', 'get_remark',
    )
    list_per_page = 40
    save_as_continue = False
    date_hierarchy = 'billing_date'
    readonly_fields = invoice_info
    form = SendInvoicesForm
    list_filter = (('invoice_id__fill_date', DateRangeFilter),
                   'invoice_id__salesman')
    resource_class = SendInvoiceResources
    list_display_links = ('get_salesman', 'get_contract_number')
    search_fields = ('invoice_number',)

    def receivables(self, obj):
        """自动计算应收金额"""
        invoice_value = self.get_invoice_value(obj)
        receive_value = self.get_receive_value(obj)
        if invoice_value is None:
            invoice_value = 0
        if receive_value is None:
            receive_value = 0
        money = invoice_value - receive_value
        return format_html('<span>{}</span>', money)
    receivables.short_description = "应收金额"

    def get_apply_name(self, obj):
        return obj.invoice_id.apply_name
    get_apply_name.short_description = "申请人"

    def get_salesman(self, obj):
        return obj.invoice_id.salesman
    get_salesman.short_description = "业务员"

    def get_contract_number(self, obj):
        invoice_data = InvoiceInfo.objects.get(id=obj.invoice_id.id)
        if invoice_data.contract_id is not None:
            return invoice_data.contract_id.contract_number
        else:
            return '-'
    get_contract_number.short_description = "合同号"

    def get_invoice_type(self, obj):
        return obj.invoice_id.invoice_type
    get_invoice_type.short_description = "发票类型"

    def get_invoice_issuing(self, obj):
        issuing_entities = {'shry': "上海锐翌", 'hzth': "杭州拓宏", 'hzry': "杭州锐翌",
                            'sdry': "山东锐翌"}
        return issuing_entities[obj.invoice_id.invoice_issuing]
    get_invoice_issuing.short_description = "开票单位"

    def get_invoice_title(self, obj):
        return obj.invoice_id.invoice_title
    get_invoice_title.short_description = "发票抬头"

    def get_tariff_item(self, obj):
        return obj.invoice_id.tariff_item
    get_tariff_item.short_description = "税号"

    def get_send_address(self, obj):
        return obj.invoice_id.send_address
    get_send_address.short_description = "对方地址"

    def get_address_phone(self, obj):
        return obj.invoice_id.address_phone
    get_address_phone.short_description = "电话"

    def get_opening_bank(self, obj):
        return obj.invoice_id.opening_bank
    get_opening_bank.short_description = "开户行"

    def get_bank_account_number(self, obj):
        return obj.invoice_id.bank_account_number
    get_bank_account_number.short_description = "账号"

    def get_invoice_value(self, obj):
        return obj.invoice_id.invoice_value
    get_invoice_value.short_description = "开票金额"

    def get_receive_date(self, obj):
        payment_date = None
        payment = obj.paymentinfo_set.exclude(receive_date__exact=None)
        payment_order = payment.order_by('-receive_date')
        if len(payment_order) > 0:
            payment_date = payment_order[0].receive_date
        return payment_date
    get_receive_date.short_description = "到账时间"

    def get_receive_value(self, obj):
        payment_sum = 0
        receive_data = obj.paymentinfo_set.exclude(receive_value__exact=None)
        if receive_data is not None:
            for payment in receive_data:
                payment_sum += payment.receive_value
        return payment_sum
    get_receive_value.short_description = "到账金额"

    def get_invoice_content(self, obj):
        return obj.invoice_id.invoice_content
    get_invoice_content.short_description = "开票内容"

    def get_remark(self, obj):
        return obj.invoice_id.remark
    get_remark.short_description = "备注"

    @staticmethod
    def statistic_invoice_value(qs):
        """按时间段统计开票额及到款额"""
        invoice_values = 0
        receive_values = 0
        if qs is not None:
            for data in qs:
                invoice_data = InvoiceInfo.objects.get(id=data.invoice_id.id)
                if invoice_data.invoice_value is not None:
                    invoice_values += invoice_data.invoice_value
                payment_data = data.paymentinfo_set.exclude(receive_value__exact=None)
                if payment_data is not None:
                    for payment in payment_data:
                        receive_values += payment.receive_value
        return invoice_values, receive_values

    def get_readonly_fields(self, request, obj=None):
        # TODO: hasattr函数的隐含作用，在执行hasattr之前obj.name出现属性不存在错误
        # TODO：但执行后正常，为啥呢？
        self.readonly_fields = self.invoice_info
        # if obj:
        if hasattr(obj, 'send_flag'):
            if obj.send_flag:
                self.readonly_fields = self.invoice_info + self.send_invoice_info
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        send_invoice = SendInvoices.objects.filter(pk=object_id)
        self.get_readonly_fields(request, obj=send_invoice)
        return super(SendInvoiceAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # TODO: 查询集换为按条件过滤后的
        # 筛选后的查询集由ListFilter中的queryset()返回，但不知如何获取
        # 发现template中的数据集由ChangeList类负责显示，显示集为调用get_results()
        # 函数后result_list的值，即筛选后的查询集
        result = self.get_changelist_instance(request)
        result.get_results(request)
        # print(request.META["QUERY"])
        # queryset = self.get_queryset()
        # query_string_dict = dict(request.META["QUERY"])
        # queryset.filter(invoice_id__gte=balald)
        # 获取model中的所有查询集
        # qs = super().get_queryset(request)
        qs = result.result_list
        extra_context['invoice_values'], extra_context['receive_values'] \
            = self.statistic_invoice_value(qs)
        return super(SendInvoiceAdmin, self).changelist_view(request, extra_context)

    # def get_changeform_initial_data(self, request):
    #     initial = super(SendInvoiceAdmin, self).get_changeform_initial_data(request)
    #     initial['fill_name'] = request.user
    #     return initial

    def save_model(self, request, obj, form, change):
        if change:
            obj.fill_name = request.user
        super(SendInvoiceAdmin, self).save_model(request, obj, form, change)
