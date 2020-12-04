from django import forms
from data.models import Run
from .models import ConditionInstance

class NameForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)

class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        exclude =()

class ConditionInstanceForm(forms.ModelForm):
    class Meta:
        model = ConditionInstance
        exclude =()

ConditionInstanceFormSet = forms.inlineformset_factory(Run, ConditionInstance,
                                            form=ConditionInstanceForm, extra=1)