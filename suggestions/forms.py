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
        label=u'慢性病史',
        queryset=Choices.objects.filter(code__contains="f07"),
        widget=forms.CheckboxSelectMultiple()
    )
    
    class Meta:
        model = Collections
        fields = '__all__'
