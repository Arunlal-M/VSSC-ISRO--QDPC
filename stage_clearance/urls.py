from django.contrib import admin
from django.urls import path,include
from .views.stage_clearance_view import StageClearance

urlpatterns = [
    path('clearance', StageClearance.as_view(), name='clearance'),
]