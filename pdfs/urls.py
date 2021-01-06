from django.urls import path,re_path

from . import views

urlpatterns = [
    path('run/<int:run_pk>/', views.DownloadRunSheetPDF, name='runsheet-pdf'),
]

