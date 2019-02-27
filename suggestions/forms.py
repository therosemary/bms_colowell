from django import forms
from suggestions.models import Collections, Choices


class CollectionsForm(forms.ModelForm):
    _f05 = forms.ModelMultipleChoiceField(
        label="下消化道症状",
        queryset=Choices.objects.filter(code__contains="f05"),
        widget=forms.CheckboxSelectMultiple()
    )
    _f06 = forms.ModelMultipleChoiceField(
        label="其它病史",
        queryset=Choices.objects.filter(code__contains="f06"),
        widget=forms.CheckboxSelectMultiple()
    )
    _f07 = forms.ModelMultipleChoiceField(
        label="慢性病史",
        queryset=Choices.objects.filter(code__contains="f07"),
        widget=forms.CheckboxSelectMultiple()
    )
    t01 = forms.CharField(
        label="饮食建议",
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}),
    )
    t02 = forms.CharField(
        label="生活方式",
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}),
    )
    t03 = forms.CharField(
        label="体育锻炼",
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}),
    )
    t04 = forms.CharField(
        label="健康乐观心态",
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}),
    )
    t05 = forms.CharField(
        label="定期筛查",
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}),
    )
    t06 = forms.CharField(
        label="确诊和治疗",
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}),
    )
    t07 = forms.CharField(
        label="肠镜检查准备",
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}),
    )
    
    class Meta:
        model = Collections
        fields = '__all__'
