from django.contrib import admin
from django.urls import path,include
from .views.process import ProcessView,ProcessListView,ProcessCreateView,EditProcessStepView,DeleteProcessStepView

urlpatterns = [
    path('process_list_detail/<str:process_title>/', ProcessView.as_view(), name='process_detail'),
    path('list/', ProcessListView.as_view(), name='process_list'),
    path('create/', ProcessCreateView.as_view(), name='process_create'),
    
    path('view/<str:process_title>/<int:stepId>/', EditProcessStepView.as_view(), name='process_edit'),
    path('edit/<str:process_title>/<int:stepId>/', EditProcessStepView.as_view(), name='process_edit'),
    path('delete-step//<str:process_title>/<int:stepId>/', DeleteProcessStepView.as_view(), name='process_delete'),
]