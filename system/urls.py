from django.urls import path,re_path

from . import views

urlpatterns = [
    path('your-name/', views.get_name, name='get-name'),
    path('create-run/', views.create_run, name='create-run'),

]
