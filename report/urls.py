from django.contrib import admin
from django.urls import path,include
from .views.report_generate import ReportView, QARReportListView, ProcessLogSheetListView, ProcessLogSheetView

urlpatterns = [
path('generate_qar/<int:batch_id>/', ReportView.as_view(), name='generate_qar'),
path('qar-report-list/', QARReportListView.as_view(), name='qar-report-list'),
path('process-log-sheet-list/', ProcessLogSheetListView.as_view(), name='process-log-sheet-list'),
path('generate_process_log_sheet/<int:batch_id>/', ProcessLogSheetView.as_view(), name='generate_process_log_sheet'),
]