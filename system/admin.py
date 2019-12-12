from django.contrib import admin
from .models import StingDevice,Gas,Condition,Nozzle
from .models import Camera,Lens,OpticalFilter,CameraPosition

# Register your models here.
class GasAdmin(admin.ModelAdmin):
    list_display = ('name','abbrv','notes')
    search_fields = ('name','abbrv','notes')

class StingDeviceAdmin(admin.ModelAdmin):
    list_display = ('name','sn','size','limits','notes')
    search_fields = ('name','sn','size','limits','notes')

class ConditionAdmin(admin.ModelAdmin):
    list_display = ('name','current','plasma_gas_flow','shield_gas_flow')

class CameraAdmin(admin.ModelAdmin):
    list_display = ('name','notes')

class LensAdmin(admin.ModelAdmin):
    list_display = ('name','notes')

class OpticalFilterAdmin(admin.ModelAdmin):
    list_display = ('name','notes')

class CameraPositionAdmin(admin.ModelAdmin):
    list_display = ('name','notes')

class NozzleAdmin(admin.ModelAdmin):
    list_display = ('name','diameter','notes')

admin.site.register(Condition,ConditionAdmin)
admin.site.register(Gas,GasAdmin)
admin.site.register(StingDevice,StingDeviceAdmin)

admin.site.register(Camera,CameraAdmin)
admin.site.register(Lens,LensAdmin)
admin.site.register(OpticalFilter,OpticalFilterAdmin)
admin.site.register(CameraPosition,CameraPositionAdmin)

admin.site.register(Nozzle,NozzleAdmin)
