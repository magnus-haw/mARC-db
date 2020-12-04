from django.contrib import admin
from .models import StingDevice,Gas,Condition,Nozzle,Cathode
from .models import Camera,Lens,OpticalFilter,CameraPosition
from .models import Disk, ConditionInstance

# Register your models here.
class GasAdmin(admin.ModelAdmin):
    list_display = ('name','abbrv','notes')
    search_fields = ('name','abbrv','notes')

class StingDeviceAdmin(admin.ModelAdmin):
    list_display = ('name','diagnostic','description')
    search_fields = ('name','diagnostic','description')

class ConditionAdmin(admin.ModelAdmin):
    list_display = ('name','current','plasma_gas_flow','shield_gas_flow')

class ConditionInstanceAdmin(admin.ModelAdmin):
    list_display = ('condition','run','name','dwell_time')

class CameraAdmin(admin.ModelAdmin):
    list_display = ('name','notes')

class LensAdmin(admin.ModelAdmin):
    list_display = ('name','notes')

class OpticalFilterAdmin(admin.ModelAdmin):
    list_display = ('name','notes')

class CameraPositionAdmin(admin.ModelAdmin):
    list_display = ('name','notes')

class CathodeAdmin(admin.ModelAdmin):
    list_display = ('name','type', 'installed', 'removed')

class DiskAdmin(admin.ModelAdmin):
    list_display = ('name','notes')

class NozzleAdmin(admin.ModelAdmin):
    list_display = ('name','diameter','notes')

class PreRunSettingsAdmin(admin.ModelAdmin):
    list_display = ('name','nozzle','cathode','disks')

admin.site.register(Condition,ConditionAdmin)
admin.site.register(ConditionInstance,ConditionInstanceAdmin)
admin.site.register(Gas,GasAdmin)
admin.site.register(StingDevice,StingDeviceAdmin)

admin.site.register(Camera,CameraAdmin)
admin.site.register(Lens,LensAdmin)
admin.site.register(OpticalFilter,OpticalFilterAdmin)
admin.site.register(CameraPosition,CameraPositionAdmin)

admin.site.register(Cathode,CathodeAdmin)
admin.site.register(Disk,DiskAdmin)
admin.site.register(Nozzle,NozzleAdmin)