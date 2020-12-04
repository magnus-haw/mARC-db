from django.urls import path,re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('apparatus/', views.ApparatusListView, name='apparatus'),
    path('apparatus/<int:apparatus_pk>/', views.ApparatusDetailView, name='apparatus-detail'),
    path('apparatus/<int:apparatus_pk>/upload_xlsx/', views.upload_xlsx, name='upload_xlsx'),
    path('test/<int:test_pk>/', views.TestView, name='test'),
    path('test/<int:test_pk>/upload_csv/', views.upload_csv, name='upload_csv'),
    path('run/<int:run_pk>', views.ViewRun, name='run-detail'),
    path('diagnostic/<int:diagnostic_pk>', views.ViewDiagnostic, name='diagnostic-detail'),
    path('cathode/<int:cathode_pk>', views.CathodeView, name='cathode-detail'),
    path('nozzle/<int:nozzle_pk>', views.NozzleView, name='nozzle-detail'),
    path('disk/<int:disk_pk>', views.DiskView, name='disk-detail'),
    path('run/<int:run_pk>/download_csv/', views.DownloadRunCSV, name='run-detail-csv'),

    path('search/', views.SearchView, name='search'),
    path('search/<int:apparatus_pk>/', views.SearchData, name='search-app'),
    path('search/<int:apparatus_pk>/download_csv/', views.DownloadSearchCSV, name='search-csv'),	
]

