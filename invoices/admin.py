import datetime
from django.utils.html import format_html
from django.contrib import admin
from django.db.models import Sum, Q
from import_export.admin import ImportExportActionModelAdmin
from daterange_filter.filter import DateRangeFilter
# from django.contrib.admin.views.main import ChangeList
from projects.models import InvoiceInfo
from invoices.models import SendInvoices, PaymentInfo, TradingRecord
from invoices.forms import SendInvoicesForm
from invoices.resources import SendInvoiceResources, PaymentInfoResource


# class PaymentInline(admin.TabularInline):
#     model = PaymentInfo.send_invoice.through
#     verbose_name = verbose_name_plural = "到账信息"
#     extra = 1


class PaymentInfoAdmin(ImportExportActionModelAdmin):
    """到款信息管理"""

    # inlines = [PaymentInline]
    # exclude = ('send_invoice',)
    fields = (
        'receive_value', 'receive_date', 'contract_number', 'send_invoice',
        'flag'
    )
    list_display = (
        'payment_number', 'contract_number', 'receive_value', 'receive_date',
        'wait_invoices', 'flag'
    )
    list_per_page = 30
    save_as_continue = False
    list_display_links = ('payment_number',)
    search_fields = ('payment_number',)
    resource_class = PaymentInfoResource

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ()
        if hasattr(obj, 'flag'):
            if obj.flag:
                self.readonly_fields = ('receive_value', 'flag')
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        payment_data = PaymentInfo.objects.get(id=object_id)
        self.get_readonly_fields(request, obj=payment_data)
        return super(PaymentInfoAdmin, self).change_view(request, object_id,
                                                         form_url,
                                                         extra_context=extra_context)

    @staticmethod
    def handle_relation_id(request, obj):
        """处理当前所选发票和已选发票的id"""
        send_invoice_id = []
        before_send_invoice_id = []
        send_invoice = request.POST.get('send_invoice')
        if send_invoice is not None:
            send_invoice_id = [int(x) for x in request.POST.getlist('send_invoice')]
            # send_invoice_id.sort()
        before_send_invoice_data = obj.tradingrecord_set.all()
        if before_send_invoice_data is not None:
            for data in before_send_invoice_data:
                before_send_invoice_id.append(data.send_invoices_id_id)
        return send_invoice_id, before_send_invoice_id

    @staticmethod
    def create_middle(payment_id, send_invoices, final_receive_value=None):
        """新增中间表记录"""
        if final_receive_value is None:
            for data in send_invoices:
                # TODO:查询集是否为可迭代对象?
                TradingRecord.objects.create(send_invoices_id=data,
                                             payment_info_id_id=payment_id,
                                             transaction_amount=data.wait_payment)
        else:
            send_invoices_len = len(send_invoices)
            for data in send_invoices[0:send_invoices_len-1]:
                TradingRecord.objects.create(send_invoices_id=data,
                                             payment_info_id_id=payment_id,
                                             transaction_amount=data.wait_payment)
            TradingRecord.objects.create(send_invoices_id=send_invoices[send_invoices_len-1],
                                         payment_info_id_id=payment_id,
                                         transaction_amount=final_receive_value)

    @staticmethod
    def total_wait_payment(send_invoice_id):
        """合计当前所选发票的待到款总额"""
        wait_payment_invoices = SendInvoices.objects.filter(
            Q(id__in=send_invoice_id) & Q(wait_payment__gt=0))
        payment = wait_payment_invoices.aggregate(value=Sum('wait_payment'))
        wait_payment_value = payment.get('value', 0)
        if wait_payment_value is None:
            wait_payment_value = 0
        return wait_payment_invoices, wait_payment_value

    @staticmethod
    def update_invoice(send_invoice_id, now_wait_invoices, payment_id):
        """更新被选中的发票信息"""
        # 获取当前被选中且待到款额大于零的发票信息
        wait_payment_invoices, wait_payment_value = PaymentInfoAdmin.total_wait_payment(send_invoice_id)
        wait_send_invoices_order = wait_payment_invoices.order_by('fill_date')
        # 判断待开票额与总应收金额的大小
        if now_wait_invoices >= wait_payment_value:
            new_wait_invoices = now_wait_invoices - wait_payment_value
            if wait_send_invoices_order is not None:
                # 新增中间表记录
                PaymentInfoAdmin.create_middle(payment_id, wait_send_invoices_order)
                # TODO: new_wait_invoices_order执行更新操作后会被清空？
                wait_send_invoices_order.update(wait_payment=0)
        else:
            new_wait_invoices = now_wait_invoices
            send_invoice_len = len(wait_send_invoices_order)
            print(wait_send_invoices_order, wait_payment_value)
            if wait_payment_value - wait_send_invoices_order[send_invoice_len-1].wait_payment < now_wait_invoices:
                new_wait_invoices = 0
                # 最后一张发票的待到款额
                last_wait_payment = wait_payment_value - now_wait_invoices
                # 最后一张发票的本次到款额
                final_receive_value = wait_send_invoices_order[
                                          send_invoice_len-1].wait_payment - last_wait_payment
                # 新增中间表记录
                PaymentInfoAdmin.create_middle(payment_id,
                                               wait_send_invoices_order,
                                               final_receive_value)
                # 更新待到款额
                wait_send_invoices = wait_send_invoices_order.exclude(
                    id=wait_send_invoices_order[send_invoice_len-1].id)
                wait_send_invoices.update(wait_payment=0)
                wait_payment_invoices_last = wait_send_invoices_order.filter(
                    id=wait_send_invoices_order[send_invoice_len-1].id)
                wait_payment_invoices_last.update(wait_payment=last_wait_payment)
                # for data in new_wait_invoices_order[0:send_invoice_len-1]:
                #     data.update(wait_payemt=0)
                # new_wait_invoices_order[0:len(new_wait_invoices_order) - 1].update(wait_payment=0)
                # wait_send_invoices_order[send_invoice_len-1].update(
                #     wait_payment=last_wait_payment)
            else:
                # 所选发票无意义，结束当次更改，弹出提示信息
                pass
        return new_wait_invoices, wait_send_invoices_order

    @staticmethod
    def delete_trading_record(payment_id, delete_set):
        """删除当次未被选中的发票信息"""
        #查找中间表信息
        trading_record_data = TradingRecord.objects.filter(
            Q(send_invoices_id_id__in=delete_set) &
            Q(payment_info_id_id=payment_id))
        #查找被移除的发票信息
        update_send_invoices = SendInvoices.objects.filter(id__in=delete_set)
        print(update_send_invoices)
        if update_send_invoices is not None:
            for data in update_send_invoices:
                trading_record = trading_record_data.get(send_invoices_id_id=data.id)
                print(trading_record)
                #计算当前发票的应收额
                wait_payment_value = data.wait_payment + \
                                     trading_record.transaction_amount
                SendInvoices.objects.filter(id=data.id).update(
                    wait_payment=wait_payment_value)
                # data.update(wait_payment=wait_payment_value)
                #删除中间表记录
                trading_record.delete()
        return

    @staticmethod
    def total_invoices_value(payment_id, intersect_set):
        """合计已开票额：合计中间表的交易额"""
        trading_value = 0
        if len(intersect_set):
            trading_records = TradingRecord.objects.filter(Q(
                payment_info_id_id=payment_id) &
                Q(send_invoices_id_id__in=intersect_set))
            trading = trading_records.aggregate(trading_value=Sum(
                'transaction_amount'))
            trading_value = trading.get('trading_value', 0)
        return trading_value


    def save_model(self, request, obj, form , change):
        # 获取form页面到款额
        receive_value = float(request.POST.get('receive_value', 0))
        delete_set = []
        level_set = []
        diff_set = []
        if change:
            if obj.flag:
                # step1：获取修改前后的发票id，并求交集和差集
                send_invoice_id, before_send_invoice_id = \
                    self.handle_relation_id(request, obj)
                # 差集
                diff_set = list(set(send_invoice_id) ^ set(before_send_invoice_id))
                # 交集（保留）
                level_set = list(set(send_invoice_id) & set(before_send_invoice_id))
                # 新增
                new_set = list(set(diff_set) & set(send_invoice_id))
                # 删除
                delete_set = list(set(diff_set) & set(before_send_invoice_id))
                # step2: 计算当前待开票总额，当前到款额减去交易记录表中level_set的交易总额
                trading_value = self.total_invoices_value(obj.id, level_set)
                now_wait_invoices = receive_value - trading_value
                # step3: 计算当前所选发票的待到款总额
                wait_payment_value = self.total_wait_payment(send_invoice_id)
                # step4: 根据待开票总额与待到款总额的大小关系选择不同处理逻辑
                try:
                    # 移除当前未被选中的发票信息
                    self.delete_trading_record(obj.id, delete_set)
                    # 更新发票被分配的到款额
                    obj.wait_invoices, invoices = self.update_invoice(send_invoice_id,
                                                                 now_wait_invoices, obj.id)
                    obj.save()
                except Exception:
                    pass
            super(PaymentInfoAdmin, self).save_model(request, obj, form, change)
        else:
            if len(request.POST.getlist('send_invoice')):
                temp = 'RE' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
                obj.payment_number = temp
                super(PaymentInfoAdmin, self).save_model(request, obj,
                                                             form, change)
                if obj.flag:
                    try:
                    # 从request中获取关联的发票id并转为int类型
                        send_invoice_id = [int(x) for x in
                                           request.POST.getlist('send_invoice')]
                        print(send_invoice_id)
                        obj.wait_invoices, invoices = self.update_invoice(
                            send_invoice_id, receive_value, obj.id)
                        obj.save()
                    except Exception:
                        pass
            else:
                #新增时不选择发票的情况
                obj.wait_invoices = receive_value
                temp = 'RE' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
                obj.payment_number = temp
                super(PaymentInfoAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        trading_record_data = obj.tradingrecord_set.all()
        print(trading_record_data)
        for data in trading_record_data:
            send_invoice = SendInvoices.objects.get(id=data.send_invoices_id_id)
            print(send_invoice)
            value = send_invoice.wait_payment + data.transaction_amount
            send_invoice.wait_payment=value
            send_invoice.save()
        super(PaymentInfoAdmin, self).delete_model(request, obj)


class SendInvoiceAdmin(ImportExportActionModelAdmin):
    """
    发票寄送信息管理
    注：每条记录在发票申请提交后自动被创建
    """
    # change_list_template = 'admin/invoices/change_list_template_invoices.html'
    # inlines = [PaymentInline]
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
        'wait_payment', 'get_receive_date', 'get_invoice_title',
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
        payment_sum = obj.invoice_id.invoice_value - obj.wait_payment
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

    def delete_model(self, request, obj):
        trading_record_data = obj.tradingrecord_set.all()
        if trading_record_data is not None:
            for data in trading_record_data:
                payment_info = PaymentInfo.objects.get(id=data.payment_info_id_id)
                value = payment_info.wait_invoices + data.transaction_amount
                payment_info.update(wait_invoices=value)
        super(SendInvoiceAdmin, self).delete_model(request, obj)
