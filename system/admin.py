from django.contrib import admin
from .models import StingDevice,Gas,Condition,Nozzle,Cathode
from .models import Camera,Lens,OpticalFilter,CameraPosition
from .models import Disk, ConditionInstance, Component, Subsystem
from .models import SubsystemConfig, SubsystemConfigItem
from .models import ComponentFile

# Register your models here.
class GasAdmin(admin.ModelAdmin):
    list_display = ('name','abbrv','notes')
    search_fields = ('name','abbrv','notes')

class StingDeviceAdmin(admin.ModelAdmin):
    list_display = ('name','diagnostic','description')
    search_fields = ('name','diagnostic','description')

class ConditionAdmin(admin.ModelAdmin):
    list_display = ('name','current','plasma_gas_flow','shield_gas_flow', 'nozzle', 'disks')

class ConditionInstanceAdmin(admin.ModelAdmin):
    list_display = ('condition','run','name','dwell_time')

class CathodeAdmin(admin.ModelAdmin):
    list_display = ('name','type', 'installed', 'removed')

class DiskAdmin(admin.ModelAdmin):
    list_display = ('name','notes')

class NozzleAdmin(admin.ModelAdmin):
    list_display = ('name','diameter','notes')

class ComponentFileInline(admin.StackedInline):
    model = ComponentFile

class SubsystemConfigItemInline(admin.StackedInline):
    model = SubsystemConfigItem

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type','description','installed')
    list_filter = ('type', 'installed',)
    inlines = [ComponentFileInline,]

class SubsystemAdmin(admin.ModelAdmin):
    list_display = ('name','apparatus','type','description')
    list_filter = ('apparatus','type',)

class SubsystemConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'subsystem', 'description', 'last_modified')
    list_filter = ('subsystem',)
    inlines = [SubsystemConfigItemInline,]

admin.site.register(SubsystemConfig, SubsystemConfigAdmin)
admin.site.register(Subsystem, SubsystemAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Condition,ConditionAdmin)
admin.site.register(ConditionInstance,ConditionInstanceAdmin)
admin.site.register(Gas,GasAdmin)
admin.site.register(StingDevice,StingDeviceAdmin)

admin.site.register(Cathode,CathodeAdmin)
admin.site.register(Disk,DiskAdmin)
admin.site.register(Nozzle,NozzleAdmin)