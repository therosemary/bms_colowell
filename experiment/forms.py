from django import forms
from experiment.models import ExtExecute, QualityTest, BsTask, \
    FluorescenceQuantification


class ExtExecuteForm(forms.ModelForm):
    """提取任务表的字段限制"""

    class Meta:
        model = ExtExecute
        fields = "__all__"

    def clean_fail(self):
        sub = self.cleaned_data['submit']
        fa = self.cleaned_data["fail"]
        if sub and fa:
            raise forms.ValidationError(
                "请不要同时勾选任务完成和任务重做", code='invalid value'
            )
        else:
            return self.cleaned_data['fail']


class QualityTestForm(forms.ModelForm):
    """提取任务表的字段限制"""

    class Meta:
        model = QualityTest
        fields = "__all__"

    def clean_fail(self):
        sub = self.cleaned_data['submit']
        fa = self.cleaned_data["fail"]
        if sub and fa:
            raise forms.ValidationError(
                "请不要同时勾选任务完成和任务重做", code='invalid value'
            )
        else:
            return self.cleaned_data['fail']


class BsTaskForm(forms.ModelForm):
    """提取任务表的字段限制"""

    class Meta:
        model = BsTask
        fields = "__all__"

    def clean_fail(self):
        sub = self.cleaned_data['submit']
        fa = self.cleaned_data["fail"]
        if sub and fa:
            raise forms.ValidationError(
                "请不要同时勾选任务完成和任务重做", code='invalid value'
            )
        else:
            return self.cleaned_data['fail']


class FluorescenceQuantificationForm(forms.ModelForm):
    """提取任务表的字段限制"""

    class Meta:
        model = FluorescenceQuantification
        fields = "__all__"

    def clean_fail(self):
        sub = self.cleaned_data['submit']
        fa = self.cleaned_data["fail"]
        if sub and fa:
            raise forms.ValidationError(
                "请不要同时勾选任务完成和任务重做", code='invalid value'
            )
        else:
            return self.cleaned_data['fail']
