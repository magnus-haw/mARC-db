from django import forms
from .models import Record,Series,Test,Diagnostic

class SearchForm(forms.Form):
    tests = forms.ModelMultipleChoiceField(
            queryset = Test.objects.all(),
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

class UploadTestForm(forms.Form):
    name = forms.CharField(max_length=50)
    date = forms.DateField()
    file = forms.FileField()

class UploadRunForm(forms.Form):
    name = forms.CharField(max_length=50)
    file = forms.FileField()
