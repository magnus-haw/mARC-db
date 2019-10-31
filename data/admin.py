from django.contrib import admin
from .models import Test,Diagnostic,Run,Apparatus
from .models import Unit,AlternateUnitName,AlternateDiagnosticName
from .models import Series,Record,Person

from system.models import ConditionInstance,HeaterSettings,StingSettings
from system.models import FileAttachments,GasSettings,DistilledWaterLoop
from system.models import SensorWaterLoop,VacuumWaterLoop,VacuumSystem
from system.models import PhotoAttachment,CameraSettings

# Register your models here.


def delete_selected(modeladmin, request, queryset):
    queryset.delete()

class TestAdmin(admin.ModelAdmin):
    list_display = ('name','date','notes')
    list_filter = ('date',)
    actions = (delete_selected,)
    search_fields = ('name','test','notes')

class VacuumSystemInline(admin.TabularInline):
    model = VacuumSystem

class FileAttachmentsInline(admin.TabularInline):
    model = FileAttachments

class SensorWaterLoopInline(admin.StackedInline):
    model = SensorWaterLoop

class VacuumWaterLoopInline(admin.StackedInline):
    model = VacuumWaterLoop

class DistilledWaterLoopInline(admin.StackedInline):
    model = DistilledWaterLoop

class GasSettingsInline(admin.TabularInline):
    model = GasSettings
    
class StingSettingsInline(admin.TabularInline):
    model = StingSettings

class HeaterSettingsInline(admin.TabularInline):
    model = HeaterSettings

class ConditionInline(admin.StackedInline):
    model = ConditionInstance
    extra = 1

class PhotoAttachmentInline(admin.TabularInline):
    model = PhotoAttachment
    
class CameraInline(admin.StackedInline):
    model = CameraSettings
    extra = 2

class RunAdmin(admin.ModelAdmin):
    list_display = ('name','test','date','notes')
    list_filter = ('test__apparatus','date','test',)
    search_fields = ('name','test__name','notes')
    inlines = [
               HeaterSettingsInline,
               GasSettingsInline,
               ConditionInline,
               CameraInline,
               StingSettingsInline,
               FileAttachmentsInline,
               DistilledWaterLoopInline,
               VacuumWaterLoopInline,
               SensorWaterLoopInline,
               VacuumSystemInline,
               ]

class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name','diagnostic','run',)
    list_filter = ('run__test__apparatus','run__test','run__test__date',)
    search_fields = ('name','test__name','notes')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name','notes')
    search_fields = ('name','notes')

class ApparatusAdmin(admin.ModelAdmin):
    list_display = ('name','acronym','notes')
    search_fields = ('name','acronym','notes')

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
    list_display = ('name','apparatus','units','sensor','notes')
    list_filter = ('apparatus','units',)
    inlines = [
        AlternateDiagnosticNameInline,
    ]

admin.site.register(Series,SeriesAdmin)
admin.site.register(Unit,UnitAdmin)
admin.site.register(Apparatus,ApparatusAdmin)
admin.site.register(Test,TestAdmin)
admin.site.register(Run,RunAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(Diagnostic,DiagnosticAdmin)

