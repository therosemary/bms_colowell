import re

from django import forms

from projects.models import ContractsInfo


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
