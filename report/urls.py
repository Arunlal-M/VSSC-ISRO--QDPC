from django.contrib import admin
from django.urls import path,include
from .views.report_generate import ReportView

urlpatterns = [
    path('generate_qar', ReportView.as_view(), name='generate_qar'),
]