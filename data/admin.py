from django.contrib import admin
from .models import Test, Diagnostic, Run, Apparatus
from .models import Unit, AlternateUnitName, AlternateDiagnosticName
from .models import Person

from system.models import ConditionInstance, FileAttachments
from system.models import GasSettings, DistilledWaterLoop
from system.models import SensorWaterLoop, VacuumWaterLoop, VacuumSystem
from system.models import CameraSettings, SettingAttachment


# Register your models here

class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'notes')
    list_filter = ('date',)
    search_fields = ('name', 'test', 'notes')

class VacuumSystemInline(admin.TabularInline):
    model = VacuumSystem

# class FileAttachmentsInline(admin.TabularInline):
#     model = FileAttachments

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
        # FileAttachmentsInline,
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


class AlternateUnitNameInline(admin.TabularInline):
    model = AlternateUnitName


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')
    search_fields = ('name', 'short_name')
    inlines = [
        AlternateUnitNameInline,
    ]


class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ('name', 'apparatus', 'units', 'sensor', 'notes')
    list_filter = ('apparatus', 'units',)
    inlines = [
        AlternateDiagnosticNameInline,
    ]

admin.site.register(Unit, UnitAdmin)
admin.site.register(Apparatus, ApparatusAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Diagnostic, DiagnosticAdmin)
