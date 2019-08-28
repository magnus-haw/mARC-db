from django.contrib import admin
from .models import StingDevice,Gas,Condition

# Register your models here.
class GasAdmin(admin.ModelAdmin):
    list_display = ('name','abbrv','notes')
    search_fields = ('name','abbrv','notes')

class StingDeviceAdmin(admin.ModelAdmin):
    list_display = ('name','sn','size','limits','notes')
    search_fields = ('name','sn','size','limits','notes')

class ConditionAdmin(admin.ModelAdmin):
    list_display = ('name','current','plasma_gas_flow','shield_gas_flow','nozzle_diameter')

admin.site.register(Condition,ConditionAdmin)
admin.site.register(Gas,GasAdmin)
admin.site.register(StingDevice,StingDeviceAdmin)
