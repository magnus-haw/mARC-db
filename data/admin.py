from django.contrib import admin
from .models import Experiment,Diagnostic,Run,Facility,Apparatus
from .models import Unit,AlternateUnitName,AlternateDiagnosticName
from .models import Series,Record

# Register your models here.


def delete_selected(modeladmin, request, queryset):
    queryset.delete()

class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('name','date','notes')
    list_filter = ('date',)
    actions = (delete_selected,)
    search_fields = ('name','experiment','notes')

class RunAdmin(admin.ModelAdmin):
    list_display = ('name','experiment','notes')
    list_filter = ('experiment__date','experiment',)
    search_fields = ('name','experiment__name','notes')

class SeriesAdmin(admin.ModelAdmin):
    list_display = ('diagnostic','run',)
    list_filter = ('run__experiment__apparatus','run__experiment','run__experiment__date',)
    search_fields = ('name','experiment__name','notes')
    
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name','acronym','notes')
    search_fields = ('name','acronym','notes')

class ApparatusAdmin(admin.ModelAdmin):
    list_display = ('name','acronym','notes','facility')
    search_fields = ('name','acronym','notes','facility')

class AlternateDiagnosticNameInline(admin.TabularInline):
    model = AlternateDiagnosticName
    
class AlternateUnitNameInline(admin.TabularInline):
    model = AlternateUnitName
    
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name','short_name')
    search_fields = ('name','short_name')
    inlines = [
        AlternateUnitNameInline,
    ]

class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ('name','units','sensor','notes')
    inlines = [
        AlternateDiagnosticNameInline,
    ]

admin.site.register(Series,SeriesAdmin)
admin.site.register(Unit,UnitAdmin)
admin.site.register(Facility,FacilityAdmin)
admin.site.register(Apparatus,ApparatusAdmin)
admin.site.register(Experiment,ExperimentAdmin)
admin.site.register(Run,RunAdmin)
admin.site.register(Diagnostic,DiagnosticAdmin)

