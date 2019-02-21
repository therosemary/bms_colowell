from django import forms
from suggestions.models import F05s, F06s, F07s, Collections


class CollectionsForm(forms.ModelForm):
    _f05 = forms.ModelMultipleChoiceField(
        label="下消化道症状", queryset=F05s.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
    _f06 = forms.ModelMultipleChoiceField(
        label="其它病史", queryset=F06s.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
    _f07 = forms.ModelMultipleChoiceField(
        label=u'慢性病史', queryset=F07s.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
    
    class Meta:
        model = Collections
        fields = '__all__'
