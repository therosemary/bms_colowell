import datetime

from django.contrib import admin
from django.db.models import Q, Sum

from import_export.admin import ImportExportActionModelAdmin
from jet.filters import DateRangeFilter

from bs_invoices.models import Payment, Invoices
from bs_invoices.resources import InvoicesResources, PaymentResource
from bms_colowell.settings import COMMERCIAL_DEPARTMENT, FINANCE_DEPARTMENT


class LinkPaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    fields = (
        'receive_value', 'receive_date', 'flag'
    )
    readonly_fields = (
        'receive_value', 'receive_date', 'flag'
    )


class LinkInvoicesInline(admin.TabularInline):
    model = Invoices
    extra = 1
    invoice_info = (
        'record_number', 'salesman', 'invoice_type', 'invoice_issuing',
        'invoice_title', 'tariff_item', 'send_address', 'address_phone',
        'opening_bank', 'bank_account_number', 'invoice_value',
        'invoice_content', 'remark', 'apply_name', 'invoice_submit',
    )
    send_invoice_info = (
        'invoice_number', 'billing_date', 'invoice_send_date',
        'tracking_number', 'tax_rate', 'ele_invoice', 'send_submit'
    )
    fieldsets = (
        (u'开票信息', {
            'fields': invoice_info
        }),
        (u'寄送信息', {
            'fields': send_invoice_info
        })
    )
    readonly_fields = invoice_info + send_invoice_info


class BusinessRecordAdmin(admin.ModelAdmin):
    """交易流管理"""

    inlines = [LinkInvoicesInline, LinkPaymentInline]
    fields = (
        'contract_number',
    )

    list_display = (
        'record_number', 'contract_number', 'get_client', 'get_staff_name'
    )

    list_per_page = 40
    save_as_continue = False
    list_display_links = ('record_number',)

    def get_client(self, obj):
        client = None
        if obj.contract_number is not None:
            client = obj.contract_number.client.name
        return client
    get_client.short_description = "客户"

    def get_staff_name(self, obj):
        staff_name = None
        if obj.contract_number is not None:
            staff_name = obj.contract_number.staff_name
        return staff_name
    get_staff_name.short_description = "业务员"

    def save_model(self, request, obj, form, change):
        # print(request.POST)
        if change:
            super().save_model(request, obj, form, change)
        else:
            number = 'RE' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            obj.record_number = number
            super().save_model(request, obj, form, change)


def update_middle_deal(record_id):
    # 统计当前业务流下的总开票额及总到款额
    in_condition = Q(record_number_id=record_id) & Q(wait_payment__gt=0) &\
                   Q(send_submit=True)
    invoice_data = Invoices.objects.filter(in_condition)
    py_condition = Q(record_number_id=record_id) & Q(wait_invoices__gt=0) &\
                   Q(flag=True)
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


class InvoicesAdmin(ImportExportActionModelAdmin):
    """发票信息管理"""
    invoice_info = (
        'record_number', 'salesman', 'invoice_type', 'invoice_issuing',
        'invoice_title', 'tariff_item', 'send_address', 'address_phone',
        'opening_bank', 'bank_account_number', 'invoice_value',
        'invoice_content', 'remark', 'apply_name', 'invoice_submit',
    )
    send_invoice_info = (
        'invoice_number', 'billing_date', 'invoice_send_date',
        'tracking_number', 'tax_rate', 'ele_invoice', 'send_submit'
    )
    fieldsets = (
        (u'开票信息', {
            'fields': invoice_info
        }),
        (u'寄送信息', {
            'fields': send_invoice_info
        })
    )
    invoice_list_display = (
        'salesman', 'get_client', 'invoice_title', 'invoice_value',
        'invoice_type', 'invoice_content', 'get_receive_value',
        'get_receive_date'
    )
    list_display = (
        'salesman', 'get_contract_number', 'get_client', 'billing_date',
        'invoice_number', 'invoice_value', 'get_receive_date',
        'wait_payment', 'get_receive_date', 'invoice_title',
        'invoice_content', 'tracking_number', 'remark',
    )
    all_list_display = (
        'invoice_id', 'salesman', 'get_contract_number', 'get_client',
        'invoice_title', 'invoice_value', 'get_receive_value', 'wait_payment',
        'get_receive_date', 'invoice_type', 'invoice_content',
        'billing_date', 'invoice_number', 'tracking_number', 'remark',
    )
    list_display_links = ('invoice_id', 'salesman', 'contract_id')
    list_per_page = 40
    save_as_continue = False
    resource_class = InvoicesResources

    def get_contract_number(self, obj):
        contract_number = None
        if obj.record_number is not None:
            contract_number = obj.record_number.contract_number
        return contract_number
    get_contract_number.short_description = "合同号"

    def get_client(self, obj):
        client = None
        if obj.record_number is not None:
            client = obj.record_number.contract_number.client
        return client
    get_client.short_description = "客户"

    def get_receive_value(self, obj):
        receive_value = obj.invoice_value - obj.wait_payment
        return receive_value
    get_receive_value.short_description = "到款金额"

    def get_receive_date(self, obj):
        receive_date = None
        if obj.record_number is not None:
            business_record = obj.record_number.payment_set.all()
            business_record_order = business_record.order_by('receive_date')
            if business_record_order is not None:
                receive_date = business_record_order[0].receive_date
        return receive_date
    get_receive_date.short_description = "到款时间"

    @staticmethod
    def get_user_group(request):
        group = request.user.groups.all()
        invoice_change_permission = False
        send_change_permission = False
        for data in group:
            if data.name == COMMERCIAL_DEPARTMENT:
                invoice_change_permission = True
            if data.name == FINANCE_DEPARTMENT:
                send_change_permission = True
        return invoice_change_permission, send_change_permission

    def get_readonly_fields(self, request, obj=None):
        invoice_fields = ()
        send_fields = ()
        invoice_change_permission, send_change_permission = \
            self.get_user_group(request)
        if not invoice_change_permission:
            invoice_fields = self.invoice_info
        else:
            if hasattr(obj, 'invoice_submit'):
                if obj.invoice_submit:
                    invoice_fields = self.invoice_info
        if not send_change_permission:
            send_fields = self.send_invoice_info
        else:
            if hasattr(obj, 'send_submit') and hasattr(obj, 'invoice_submit'):
                if obj.send_submit or not obj.invoice_submit:
                    send_fields = self.send_invoice_info
        if request.user.is_superuser:
            invoice_fields = ()
            send_fields = ()
        return invoice_fields + send_fields

    def get_list_display(self, request):
        invoice_change_permission, send_change_permission = \
            self.get_user_group(request)
        if request.user.is_superuser:
            new_list_display = self.all_list_display
        elif send_change_permission:
            new_list_display = self.list_display
        else:
            new_list_display = self.invoice_list_display
        return new_list_display

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
                # TODO:改写条件，增加开票通知（同下）
                if obj.invoice_submit and obj.invoice_value == obj.wait_payment:
                    obj.wait_payment = self.invoice_middle_deal(obj)
            if hasattr(obj, 'send_value'):
                # TODO:增加开票完成通知（愈念念和销售）
                if obj.send_value:
                    pass
        else:
            number = 'FP' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            obj.invoice_id = number
            super().save_model(request, obj, form, change)
            if obj.invoice_submit:
                # TODO:发票信息填写完成，提交开票（通知财务赵静及销售）
                obj.wait_payment = self.invoice_middle_deal(obj)
            else:
                obj.wait_payment = obj.invoice_value
            if obj.send_submit:
                # TODO:增加开票完成通知（愈念念和销售）
                pass
        obj.save()

    @staticmethod
    def update_payment(paid, record_id):
        payment_data = Payment.objects.filter(record_number_id=record_id)
        payment_data_order = payment_data.order_by('-receive_date')
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


class PaymentAdmin(ImportExportActionModelAdmin):
    """到款信息管理"""

    fields = (
        'record_number', 'receive_value', 'receive_date', 'flag'
    )
    list_display = (
        'get_contract_number', 'get_client', 'receive_value', 'receive_date',
        'wait_invoices', 'flag'
    )
    list_per_page = 30
    save_as_continue = False
    list_display_links = ('get_contract_number', 'receive_value')
    search_fields = ('payment_number',)
    # resource_class = PaymentResource
    list_filter = (('receive_date', DateRangeFilter),)
    resource_class = PaymentResource

    def get_contract_number(self, obj):
        contract_number = None
        if obj.record_number is not None:
            contract_number = obj.record_number.contract_number
        return contract_number
    get_contract_number.short_description = "合同号"

    def get_client(self, obj):
        client = None
        if obj.record_number is not None:
            client = obj.record_number.contract_number.client
        return client
    get_client.short_description = "客户"

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
                # TODO:修改条件，增加到款信息提交通知（陈煜庶及销售）
                if obj.flag and obj.receive_value == obj.wait_invoices:
                    obj.wait_invoices = self.payment_middle_deal(obj)
        else:
            number = 'PY' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            obj.payment_number = number
            super().save_model(request, obj, form, change)
            if obj.flag:
                obj.wait_invoices = self.payment_middle_deal(obj)
                # TODO：增加到款信息提交通知
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
