from django.contrib import admin
from .models import Spreadsheet,Diagnostic,Sheet

# Register your models here.

admin.site.register(Spreadsheet)
admin.site.register(Sheet)
admin.site.register(Diagnostic)

