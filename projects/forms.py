import re

from django import forms
from .models import ContractsInfo, InvoiceInfo


class ContractInfoForm(forms.ModelForm):
    """合同信息表单输入限制"""

    class Meta:
        model = ContractsInfo
        fields = "__all__"

    def clean_send_back_date(self):
        """合同寄回时间应大于合同寄出时间"""
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


class InvoiceInfoForm(forms.ModelForm):
    """发票申请信息表单输入限制
       注：税率应为小数值
    """
    class Meta:
        model = InvoiceInfo
        fields = "__all__"

    def clean_tax_rate(self):
        tax_rate = self.cleaned_data['tax_rate']
        if re.match(r'0\.[0-9]+', str(tax_rate)):
            return tax_rate
        else:
            raise forms.ValidationError('税率填写错误！只能填写小于1的小数')
