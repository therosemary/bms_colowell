from django import forms
from .models import BoxApplications


class BoxApplicationsForm(forms.ModelForm):
    """盒子申请信息表单输入验证"""

    class Meta:
        model = BoxApplications
        fields = '__all__'

    def clean_intention_client(self):
        """意向代理申请盒子时，客户为必填项"""
        classification = self.cleaned_data['classification']
        intention_client = self.cleaned_data['intention_client']
        print('111111111111%s' % intention_client)
        if classification == 'YX':
            # TODO: to test "==" and "is"
            if intention_client is None:
                raise forms.ValidationError('该申请为意向代理申请，客户信息为必填项，请填写！')
        return intention_client
