from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect
from data.models import Run, Test, Apparatus, Diagnostic, Person
from .models import *
from .forms import NameForm,RunForm

# Create your views here.
def get_name(request):
    # POST request: process data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = NameForm(request.POST)
        #validate data
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to new url
            
            return render(request, "system/name.html",
                      context={
                          "success":True,
                          "show_response":True,
                          "form":form,
                          })
    # For GET or other types create blank form
    else:
        form = NameForm()
        
    
    return render(request, 'system/name.html', {'form':form})

def create_run(request):
    # POST request: process data
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = RunForm(request.POST)
        #validate data
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to new url
            new_run = form.save(commit=True)
            
            return HttpResponseRedirect(reverse('data.views.ViewRun', args=(new_run.pk,)))
    # For GET or other types create blank form
    else:
        form = RunForm()
    
    return render(request, 'system/run.html', {'form':form})