from django.contrib import admin

# Register your models here.
from .models import ConditionInstanceFit, SeriesStableStats, LinearModel
from .models import SeriesStartupStats, DiagnosticConditionAverage, RunUsage

class FitAdmin(admin.ModelAdmin):
    list_display = ('instance', 'start', 'stable_start', 'stable_end', 'end', 'notes')
    search_fields = ('instance__condition__name', 'notes')

admin.site.register(ConditionInstanceFit, FitAdmin)
admin.site.register(SeriesStableStats)
admin.site.register(SeriesStartupStats)
admin.site.register(DiagnosticConditionAverage)
admin.site.register(LinearModel)
admin.site.register(RunUsage)