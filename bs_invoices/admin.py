import datetime

from django.contrib import admin
from django.db.models import Q, Sum

from import_export.admin import ImportExportModelAdmin
from jet.filters import DateRangeFilter

from bs_invoices.models import Payment, Invoices


class LinkPaymentInline(admin.StackedInline):
    model = Payment
    extra = 1
    fields = (
        'receive_value', 'receive_date', 'flag'
    )
    readonly_fields = (
        'receive_value', 'receive_date', 'flag'
    )


class LinkInvoicesInline(admin.StackedInline):
    model = Invoices
    extra = 1
    invoice_info = (
        'contract_id', 'salesman', 'invoice_type', 'invoice_issuing',
        'invoice_title', 'tariff_item', 'send_address', 'address_phone',
        'opening_bank', 'bank_account_number', 'invoice_value',
        'invoice_content', 'remark', 'apply_name', 'flag', 'approve_flag',
    )
    send_invoice_info = (
        'invoice_number', 'billing_date', 'invoice_send_date',
        'tracking_number', 'tax_rate', 'ele_invoice', 'send_flag'
    )
    fieldsets = (
        (u'开票信息', {
            'fields': invoice_info
        }),
        (u'寄送信息', {
            'fields': send_invoice_info
        })
    )


class BusinessRecordAdmin(ImportExportModelAdmin):
    """交易流管理"""

    inlines = [LinkInvoicesInline, LinkPaymentInline]
    fields = (
        'contract_number',
    )

    list_display = (
        'record_number', 'contract_number',
    )

    list_per_page = 40
    save_as_continue = False
    list_display_links = ('record_number',)

    def save_model(self, request, obj, form, change):
        # print(request.POST)
        if change:
            super().save_model(request, obj, form, change)
        else:
            number = 'RE' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            obj.record_number = number
            super().save_model(request, obj, form, change)


def update_middle_deal(record_id):
    # TODO: 判断当前发票是否已提交；金额分配逻辑考虑不全
    # 统计当前业务流下的总开票额及总到款额
    in_condition = Q(record_number_id=record_id) & Q(wait_payment__gt=0)
    invoice_data = Invoices.objects.filter(in_condition)
    py_condition = Q(record_number_id=record_id) & Q(wait_invoices__gt=0)
    payment_data = Payment.objects.filter(py_condition)
    sum_payment = invoice_data.aggregate(value=Sum('wait_payment'))
    sum_wait_payment = sum_payment.get('value', 0)
    sum_invoices = payment_data.aggregate(value=Sum('wait_invoices'))
    sum_wait_invoices = sum_invoices.get('value', 0)

    # 计算当前业务流下的到款记录的待开票额及开票记录的待到款额
    if sum_wait_payment is not None and sum_wait_invoices is not None:
        if sum_wait_invoices >= sum_wait_payment:
            invoice_data.update(wait_payment=0)
            payment_data_order = payment_data.order_by('receive_date')
            index = 0
            while sum_wait_payment > 0:
                now_payment = payment_data_order[index]
                new_wait_invoices = now_payment.wait_invoices
                if sum_wait_payment > new_wait_invoices:
                    sum_wait_payment = sum_wait_payment - new_wait_invoices
                    new_wait_invoices = 0
                else:
                    new_wait_invoices = new_wait_invoices - sum_wait_payment
                    sum_wait_payment = 0
                index = index + 1
                now_id = now_payment.id
                payment_data.filter(id=now_id).update(
                    wait_invoices=new_wait_invoices)
        else:
            payment_data.update(wait_invoices=0)
            invoice_data_order = invoice_data.order_by('billing_date')
            index = 0
            while sum_wait_invoices > 0:
                now_invoice = invoice_data_order[index]
                new_wait_payment = now_invoice.wait_payment
                if sum_wait_invoices > new_wait_payment:
                    sum_wait_invoices = sum_wait_invoices - new_wait_payment
                    new_wait_payment = 0
                else:
                    new_wait_payment = new_wait_payment - sum_wait_invoices
                    sum_wait_invoices = 0
                index = index + 1
                now_id = now_invoice.id
                invoice_data.filter(id=now_id).update(wait_payment=new_wait_payment)


class InvoicesAdmin(ImportExportModelAdmin):
    """发票信息管理"""
    invoice_info = (
        'record_number', 'salesman', 'invoice_type', 'invoice_issuing',
        'invoice_title', 'tariff_item', 'send_address', 'address_phone',
        'opening_bank', 'bank_account_number', 'invoice_value',
        'invoice_content', 'remark', 'apply_name', 'flag', 'approve_flag',
    )
    send_invoice_info = (
        'invoice_number', 'billing_date', 'invoice_send_date',
        'tracking_number', 'tax_rate', 'ele_invoice', 'send_flag'
    )
    fieldsets = (
        (u'开票信息', {
            'fields': invoice_info
        }),
        (u'寄送信息', {
            'fields': send_invoice_info
        })
    )
    list_display = (
        'invoice_id', 'salesman', 'contract_id', 'billing_date',
        'invoice_number', 'invoice_value', 'wait_payment', 'invoice_title',
        'invoice_content', 'tracking_number', 'remark',
    )
    list_display_links = ('invoice_id',)
    list_per_page = 40
    save_as_continue = False

    @staticmethod
    def invoice_middle_deal(obj):
        wait_payment = obj.invoice_value
        condition = Q(record_number=obj.record_number) & Q(wait_invoices__gt=0)
        payment_data = Payment.objects.filter(condition)
        payment_data_order = payment_data.order_by('receive_date')
        invoice = payment_data.aggregate(value=Sum('wait_invoices'))
        sum_wait_invoices = invoice.get('value', 0)
        if sum_wait_invoices is not None:
            while wait_payment > 0 and sum_wait_invoices > 0:
                now_wait_invoices = payment_data_order[0].wait_invoices
                if wait_payment > now_wait_invoices:
                    wait_payment = wait_payment - now_wait_invoices
                    sum_wait_invoices = sum_wait_invoices - now_wait_invoices
                    new_wait_invoices = 0
                else:
                    new_wait_invoices = now_wait_invoices - wait_payment
                    wait_payment = 0
                now_id = payment_data_order[0].id
                payment_data.filter(id=now_id).update(
                    wait_invoices=new_wait_invoices)
        return wait_payment

    def save_model(self, request, obj, form, change):
        if change:
            super().save_model(request, obj, form, change)
            if hasattr(obj, 'invoice_value') and hasattr(obj, 'wait_payment'):
                if obj.flag and obj.invoice_value == obj.wait_payment:
                    obj.wait_payment = self.invoice_middle_deal(obj)
        else:
            number = 'FP' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            obj.invoice_id = number
            super().save_model(request, obj, form, change)
            if obj.flag:
                obj.wait_payment = self.invoice_middle_deal(obj)
            else:
                obj.wait_payment = obj.invoice_value
        obj.save()

    @staticmethod
    def update_payment(paid, record_id):
        payment_data = Payment.objects.filter(record_number_id=record_id)
        payment_data_order = payment_data.order_by('-receive_date')
        print(payment_data_order, paid)
        if payment_data is not None:
            index = 0
            while paid > 0:
                now_payment = payment_data_order[index]
                invoice_amount = now_payment.receive_value - \
                                 now_payment.wait_invoices
                if paid > invoice_amount:
                    new_wait_invoice = now_payment.wait_invoices + \
                                       invoice_amount
                    paid = paid - invoice_amount
                else:
                    new_wait_invoice = now_payment.wait_invoices + paid
                    paid = 0
                index = index + 1
                now_id = now_payment.id
                payment_data.filter(id=now_id).update(
                    wait_invoices=new_wait_invoice)
                print(paid)

    def delete_model(self, request, obj):
        record_id = obj.record_number.id
        paid = 0
        if hasattr(obj, 'invoice_value') and hasattr(obj, 'wait_payment'):
            paid = obj.invoice_value - obj.wait_payment
        self.update_payment(paid, record_id)
        update_middle_deal(record_id)
        super().delete_model(request, obj)


class PaymentAdmin(ImportExportModelAdmin):
    """到款信息管理"""

    fields = (
        'record_number', 'receive_value', 'receive_date', 'flag'
    )
    list_display = (
        'payment_number', 'receive_value', 'receive_date', 'wait_invoices',
        'flag'
    )
    list_per_page = 30
    save_as_continue = False
    list_display_links = ('payment_number',)
    search_fields = ('payment_number',)
    # resource_class = PaymentResource
    list_filter = (('receive_date', DateRangeFilter),)

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ()
        if hasattr(obj, 'flag'):
            if obj.flag:
                self.readonly_fields = (
                    'receive_value', 'receive_date', 'contract_number', 'flag'
                )
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        payment_data = Payment.objects.get(id=object_id)
        self.get_readonly_fields(request, obj=payment_data)
        return super().change_view(request, object_id, form_url,
                                   extra_context=extra_context)

    @staticmethod
    def payment_middle_deal(obj):
        wait_invoice = obj.receive_value
        condition = Q(record_number=obj.record_number) & Q(wait_payment__gt=0)
        invoice_data = Invoices.objects.filter(condition)
        invoice_data_order = invoice_data.order_by('billing_date')
        payment = invoice_data.aggregate(value=Sum('wait_payment'))
        sum_wait_payment = payment.get('value', 0)
        if sum_wait_payment is not None:
            index = 0
            while wait_invoice > 0 and sum_wait_payment > 0:
                now_wait_payment = invoice_data_order[index].wait_payment
                if wait_invoice > now_wait_payment:
                    wait_invoice = wait_invoice - now_wait_payment
                    sum_wait_payment = sum_wait_payment - now_wait_payment
                    new_wait_payment = 0
                else:
                    new_wait_payment = now_wait_payment - wait_invoice
                    wait_invoice = 0
                # TODO: invoice_data为动态查询？
                now_id = invoice_data_order[index].id
                invoice_data.filter(id=now_id).update(
                    wait_payment=new_wait_payment)
                # TODO: 直接按下标无法保存数据
                # invoice_data_order[index].save()
        return wait_invoice

    def save_model(self, request, obj, form, change):
        if change:
            super().save_model(request, obj, form, change)
            if hasattr(obj, 'receive_value') and hasattr(obj, 'wait_invoices'):
                if obj.flag and obj.receive_value == obj.wait_invoices:
                    obj.wait_invoices = self.payment_middle_deal(obj)
        else:
            number = 'PY' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            obj.payment_number = number
            super().save_model(request, obj, form, change)
            if obj.flag:
                obj.wait_invoices = self.payment_middle_deal(obj)
            else:
                obj.wait_invoices = obj.receive_value
        obj.save()

    @staticmethod
    def update_invoice(invoice_amount, record_id):
        invoice_data = Invoices.objects.filter(record_number_id=record_id)
        invoice_data_order = invoice_data.order_by(
            '-billing_date', 'invoice_fill_date'
        )
        if invoice_data is not None:
            index = 0
            while invoice_amount > 0:
                now_invoice = invoice_data_order[index]
                now_invoice_amount = now_invoice.invoice_value - \
                                     now_invoice.wait_payment
                if invoice_amount > now_invoice_amount:
                    new_wait_payment = 0
                    invoice_amount = invoice_amount - now_invoice_amount
                else:
                    new_wait_payment = now_invoice.wait_payment + invoice_amount
                    invoice_amount = 0
                index = index + 1
                now_id = now_invoice.id
                invoice_data.filter(id=now_id).update(
                    wait_payment=new_wait_payment)


    def delete_model(self, request, obj):
        record_id = obj.record_number.id
        invoice_amount = 0
        if hasattr(obj, 'receive_value') and hasattr(obj, 'wait_invoices'):
            invoice_amount = obj.receive_value - obj.wait_invoices
        self.update_invoice(invoice_amount, record_id)
        update_middle_deal(record_id)
        super().delete_model(request, obj)
