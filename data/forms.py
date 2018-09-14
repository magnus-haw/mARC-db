from django import forms
from .models import Record,Sheet,Spreadsheet,Diagnostic

class SearchForm(forms.Form):
    choices = Spreadsheet.objects.all().values_list('pk',flat=True)
    
    spreadsheets = forms.ModelMultipleChoiceField( 
            queryset = Spreadsheet.objects.all(),
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
