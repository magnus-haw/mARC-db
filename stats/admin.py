from django.contrib import admin

# Register your models here.
from .models import ConditionInstanceFit, SeriesStableStats
from .models import SeriesStartupStats

class FitAdmin(admin.ModelAdmin):
    list_display = ('instance', 'start', 'stable_start', 'stable_end', 'end', 'notes')
    search_fields = ('instance__condition__name', 'notes')

admin.site.register(ConditionInstanceFit, FitAdmin)