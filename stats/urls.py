from django.urls import path,re_path

from . import views

urlpatterns = [
    path('condition/<int:condition_pk>', views.ConditionView, name='condition-detail'),	
]

