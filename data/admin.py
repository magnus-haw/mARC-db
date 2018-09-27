from django.contrib import admin
from .models import Spreadsheet,Diagnostic,Sheet

# Register your models here.
class SpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('filename','date','notes')
    list_filter = ('date',)
    search_fields = ('name','spreadsheet','notes')

class SheetAdmin(admin.ModelAdmin):
    exclude = ('columnBooleans',)
    list_display = ('name','spreadsheet','avg_current','std_current','avg_voltage','avg_column_pressure','avg_plasma_gas','avg_shield_gas','notes')
    list_filter = ('spreadsheet__date','spreadsheet',)
    search_fields = ('name','spreadsheet__filename','notes')

class DiagnosticAdmin(admin.ModelAdmin):
    exclude = ('key',)
    list_display = ('key','units','sensor','notes')

admin.site.register(Spreadsheet)
admin.site.register(Sheet,SheetAdmin)
admin.site.register(Diagnostic,DiagnosticAdmin)

