from django.urls import path,re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.SearchData, name='search'),
    path('experiments/', views.ExperimentListView.as_view(), name='experiments'),
    path('experiment/<str:pk>', views.ExperimentDetailView.as_view(), name='experiment-detail'),
    path('diagnostics/', views.DiagnosticListView.as_view(), name='diagnostics'),
    path('run/<int:pk>', views.ViewSheet, name='run-detail'),
    path('run/<int:pk>/download_csv/', views.DownloadSheetCSV, name='run-detail-csv'),
    path('search/download_csv/', views.DownloadSearchCSV, name='search-csv'),
    path('diagnostic/<int:pk>', views.ViewDiagnostic, name='diagnostic-detail'),
]

