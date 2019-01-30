from django import forms
from .models import SendInvoices


class SendInvoicesForm(forms.ModelForm):
    """发票寄送信息表单输入限制"""

    class Meta:
        model = SendInvoices
        fields = "__all__"

    def clean_invoice_send_date(self):
        """开票日期应小于寄出日期"""
        billing_date = self.cleaned_data['billing_date']
        invoice_send_date = self.cleaned_data['invoice_send_date']
        if billing_date and invoice_send_date:
            if billing_date > invoice_send_date:
                raise forms.ValidationError('填写错误！发票寄出时间应大于开票时间')
        return invoice_send_date
