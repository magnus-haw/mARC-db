from django.urls import path,re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.SearchData, name='search'),
    path('spreadsheets/', views.SpreadsheetListView.as_view(), name='spreadsheets'),
    path('spreadsheet/<str:pk>', views.SpreadsheetDetailView.as_view(), name='spreadsheet-detail'),
    path('diagnostics/', views.DiagnosticListView.as_view(), name='diagnostics'),
    path('sheet/<int:pk>', views.ViewSheet, name='sheet-detail'),
    path('sheet/<int:pk>/download_csv/', views.DownloadSheetCSV, name='sheet-detail-csv'),
    path('search/download_csv/', views.DownloadSearchCSV, name='search-csv'),
    path('diagnostic/<int:pk>', views.ViewDiagnostic, name='diagnostic-detail'),
]

