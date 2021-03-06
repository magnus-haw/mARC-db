from django.contrib import admin
from .models import Test, Diagnostic, Run, Apparatus
from .models import AlternateDiagnosticName, DiagnosticFile
from .models import Person

from system.models import ConditionInstance
from system.models import GasSettings, DistilledWaterLoop
from system.models import SensorWaterLoop, VacuumWaterLoop, VacuumSystem
from system.models import CameraSettings, SettingAttachment


# Register your models here

class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'apparatus', 'date', 'notes')
    list_filter = ('date','apparatus')
    search_fields = ('name', 'test', 'notes')

class VacuumSystemInline(admin.TabularInline):
    model = VacuumSystem

class SettingAttachmentsInline(admin.TabularInline):
    model = SettingAttachment
    extra =0

class SensorWaterLoopInline(admin.StackedInline):
    model = SensorWaterLoop


class VacuumWaterLoopInline(admin.StackedInline):
    model = VacuumWaterLoop


class DistilledWaterLoopInline(admin.StackedInline):
    model = DistilledWaterLoop


class GasSettingsInline(admin.TabularInline):
    model = GasSettings

class ConditionInline(admin.StackedInline):
    model = ConditionInstance
    extra = 0

class CameraInline(admin.StackedInline):
    model = CameraSettings
    extra = 0

class RunAdmin(admin.ModelAdmin):
    list_display = ('name', 'test', 'date', 'notes')
    list_filter = ('test__apparatus', 'date', 'test',)
    search_fields = ('name', 'test__name', 'notes')
    inlines = [
        ConditionInline,
        GasSettingsInline,
        CameraInline,
        SettingAttachmentsInline,
        DistilledWaterLoopInline,
        VacuumWaterLoopInline,
        SensorWaterLoopInline,
        VacuumSystemInline,
    ]

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'notes')
    search_fields = ('name', 'notes')

class ApparatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'acronym', 'notes')
    search_fields = ('name', 'acronym', 'notes')

class AlternateDiagnosticNameInline(admin.TabularInline):
    model = AlternateDiagnosticName

class DiagnosticFileInline(admin.TabularInline):
    model = DiagnosticFile

class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ('name', 'apparatus', 'units', 'sensor', 'notes')
    list_filter = ('apparatus', 'units',)
    inlines = [
        AlternateDiagnosticNameInline,
    ]

admin.site.register(Apparatus, ApparatusAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Diagnostic, DiagnosticAdmin)
