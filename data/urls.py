from django.urls import path,re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('facilities/', views.FacilitiesView, name='facilities'),
    path('<str:facility_name>', views.FacilityDetailView, name='facility-detail'),
    path('apparatus/<int:apparatus_pk>/', views.ApparatusView, name='apparatus'),
    path('apparatus/<int:apparatus_pk>/upload_xlsx/', views.upload_xlsx, name='upload_xlsx'),
    path('experiment/<int:experiment_pk>/', views.ExperimentView, name='experiment'),
    path('experiment/<int:experiment_pk>/upload_csv/', views.upload_csv, name='upload_csv'),
    path('run/<int:run_pk>', views.ViewRun, name='run-detail'),
    path('run/<int:run_pk>/download_csv/', views.DownloadRunCSV, name='run-detail-csv'),

    path('search/', views.SearchView, name='search'),
    path('search/<int:apparatus_pk>/', views.SearchData, name='search-app'),
    path('search/<int:apparatus_pk>/download_csv/', views.DownloadSearchCSV, name='search-csv'),
    #path('experiments/', views.ExperimentListView.as_view(), name='experiments'),
    #path('experiment/<str:pk>', views.ExperimentDetailView.as_view(), name='experiment-detail'),
    #path('diagnostics/', views.DiagnosticListView.as_view(), name='diagnostics'),
    #path('diagnostic/<int:pk>', views.ViewDiagnostic, name='diagnostic-detail'),
    #
    #
]

