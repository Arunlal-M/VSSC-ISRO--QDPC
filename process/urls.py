from django.contrib import admin
from django.urls import path,include
from .views.process import ProcessView,ProcessListView,ProcessCreateView,EditProcessStepView,DeleteProcessStepView,ProcessViewSet,ProcessStepViewSet

urlpatterns = [
    path('process_list_detail/<str:process_title>/', ProcessView.as_view(), name='process_detail'),
    path('list/', ProcessListView.as_view(), name='process_list'),
    path('create/', ProcessCreateView.as_view(), name='process_create'),
    path('by-product/<int:productId>/', ProcessViewSet.as_view(), name='process_by_product'),
    path('by-process-title/<str:process_title>/', ProcessStepViewSet.as_view(), name='by_process_title'),
    

    path('view/<str:process_title>/<int:stepId>/', EditProcessStepView.as_view(), name='process_edit'),
    path('edit/<str:process_title>/<int:stepId>/', EditProcessStepView.as_view(), name='process_edit'),
    path('delete-step/<str:process_title>/<int:stepId>/', DeleteProcessStepView.as_view(), name='process_delete'),
]