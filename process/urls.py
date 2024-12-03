from django.contrib import admin
from django.urls import path,include
from .views.process import ProcessView,ProcessListView,ProcessCreateView

urlpatterns = [
    path('process_list_detail/<str:process_title>/', ProcessView.as_view(), name='process_detail'),
    path('list/', ProcessListView.as_view(), name='process_list'),
    path('create/', ProcessCreateView.as_view(), name='process_create'),
]