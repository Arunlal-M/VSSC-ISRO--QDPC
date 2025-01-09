from django.contrib import admin
from django.urls import path,include
from .views.process import ProcessView,ProcessListView,ProcessCreateView,EditProcessStepView

urlpatterns = [
    path('process_list_detail/<str:process_title>/', ProcessView.as_view(), name='process_detail'),
    path('list/', ProcessListView.as_view(), name='process_list'),
    path('create/', ProcessCreateView.as_view(), name='process_create'),
    path('edit/<int:batch_id>/', EditProcessStepView.as_view(), name='process_edit'),
]