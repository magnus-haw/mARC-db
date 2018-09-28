from django import forms
from .models import Record,Series,Experiment,Diagnostic

class SearchForm(forms.Form):
    choices = Experiment.objects.all().values_list('pk',flat=True)
    
    experiments = forms.ModelMultipleChoiceField( 
            queryset = Experiment.objects.all(),
            required=False,
            )
    #sheets = forms.MultipleChoiceField(
    #        label='Sheets:',
    #        widget=forms.CheckboxSelectMultiple,
    #        choices= Sheet.objects.all()
    #        )
    diagnostics = forms.ModelMultipleChoiceField(
            queryset = Diagnostic.objects.all(),
            required=False,
            )
