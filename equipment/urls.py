from django.contrib import admin
from django.urls import path,include
from .views.equipment_view import EquipmentView,EquipmentList,DeleteEquipmentView,AddEquipmentDocumentView



urlpatterns = [

path('equipment-add/', EquipmentView.as_view(), name='equipment-add'),
path('equipment-add/<int:equipId>/', EquipmentView.as_view(), name='equipment-update'),
path('equipment-list/', EquipmentList.as_view(), name='equipment-list'),
path('equipment-list/<int:equipId>/', DeleteEquipmentView.as_view(), name='equipment-delete'),
# path('equipment-list/delete/<int:equipId>/', DeleteEquipmentView.as_view(), name='equipment-list'),
path('equipment-document/add/', AddEquipmentDocumentView.as_view(), name='add-equipment-document'),

]


