import re

from django import forms

from projects.models import ContractsInfo, InvoiceInfo


class ContractInfoForm(forms.ModelForm):
    """合同信息表单输入验证"""

    class Meta:
        model = ContractsInfo
        fields = '__all__'

    def clean_send_back_date(self):
        """合同寄回时间应晚于合同寄出时间"""
        send_date = self.cleaned_data['send_date']
        send_back_date = self.cleaned_data['send_back_date']
        if send_date and send_back_date:
            if send_date > send_back_date:
                raise forms.ValidationError(
                    '时间输入错误，请检测！合同寄回时间应大于寄出时间'
                )
        return send_back_date


    def clean_tracking_number(self):
        """邮寄时间填写后限制邮寄单号为必填项"""
        send_date = self.cleaned_data['send_date']
        tracking_number = self.cleaned_data['tracking_number']
        if send_date and tracking_number is None:
            raise forms.ValidationError('邮寄单号为必填项，请输入！')
        return tracking_number

    def clean_end_date(self):
        """合同截止日期应晚于起始日期"""
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("合同截止日期应大于起始日期，请检查！")


class InvoiceInfoForm(forms.ModelForm):
    """发票申请信息表单输入验证"""

    class Meta:
        model = InvoiceInfo
        fields = '__all__'

    def clean_tax_rate(self):
        """税率应为小数值"""
        tax_rate = self.cleaned_data['tax_rate']
        if tax_rate is not None:
            if not re.match(r'0\.[0-9]+', str(tax_rate)):
                raise forms.ValidationError("税率填写错误！只能填写小于1的小数")
        return tax_rate

    def clean_invoice_value(self):
        """限制开票金额不能为空"""
        invoice_value = self.cleaned_data['invoice_value']
        if invoice_value is None:
            raise forms.ValidationError("开票金额不能为空")
        if invoice_value is not None and invoice_value <= 0:
            raise forms.ValidationError("开票金额不能为负数，必须大于0，请检查！")
        return invoice_value
