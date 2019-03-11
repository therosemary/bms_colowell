from django import forms
from suggestions.models import Collections, Choices


class CollectionsForm(forms.ModelForm):
    # _f05 = forms.ModelMultipleChoiceField(
    #     label="下消化道症状",
    #     queryset=Choices.objects.filter(code__contains="f05"),
    #     widget=forms.CheckboxSelectMultiple()
    # )
    # _f06 = forms.ModelMultipleChoiceField(
    #     label="其它病史",
    #     queryset=Choices.objects.filter(code__contains="f06"),
    #     widget=forms.CheckboxSelectMultiple()
    # )
    # _f07 = forms.ModelMultipleChoiceField(
    #     label="慢性病史",
    #     queryset=Choices.objects.filter(code__contains="f07"),
    #     widget=forms.CheckboxSelectMultiple()
    # )
    t01 = forms.CharField(
        label="饮食建议", required=False,
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 5}),
    )
    t02 = forms.CharField(
        label="生活方式", required=False,
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 5}),
    )
    t03 = forms.CharField(
        label="体育锻炼", required=False,
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 5}),
    )
    t04 = forms.CharField(
        label="健康乐观心态", required=False,
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 5}),
    )
    t05 = forms.CharField(
        label="定期筛查", required=False,
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 5}),
    )
    t06 = forms.CharField(
        label="确诊和治疗", required=False,
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 5}),
    )
    t07 = forms.CharField(
        label="肠镜检查准备", required=False,
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 5}),
    )
    t01 = forms.CharField(
        label="饮食建议", required=False,
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}),
    )
    t02 = forms.CharField(
        label="生活方式", required=False,
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}),
    )
    t03 = forms.CharField(
        label="体育锻炼", required=False,
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}),
    )
    t04 = forms.CharField(
        label="健康乐观心态", required=False,
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}),
    )
    t05 = forms.CharField(
        label="定期筛查", required=False,
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}),
    )
    t06 = forms.CharField(
        label="确诊和治疗", required=False,
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}),
    )
    t07 = forms.CharField(
        label="肠镜检查准备", required=False,
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}),
    )
    
    class Meta:
        model = Collections
        fields = '__all__'
