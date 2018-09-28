from django.contrib import admin
from .models import Experiment,Diagnostic,Run

# Register your models here.
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('name','date','notes')
    list_filter = ('date',)
    search_fields = ('name','experiment','notes')

class RunAdmin(admin.ModelAdmin):
    list_display = ('name','experiment','notes')
    list_filter = ('experiment__date','experiment',)
    search_fields = ('name','experiment__name','notes')

class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ('units','sensor','notes')

admin.site.register(Experiment)
admin.site.register(Run,RunAdmin)
admin.site.register(Diagnostic,DiagnosticAdmin)

