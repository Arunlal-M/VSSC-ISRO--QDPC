from django.contrib import admin
from .views.consumable import ConsumableAdd,ConsumableByid
from.views.consumable import ConsumableListFetchView,ConsumableDetailView,DeleteConsumableView,UpdateConsumableStatusView,ViewConsumableDetailView,AddConsumableDocumentView
from .views.consumable_batch import ConsumableBatchFetchView,ConsumableBatchAddView,ConsumableBatchDetailView,ViewConsumableBatchDetailView,ConsumableBatchEditView,DeleteConsumableBatchView,ConsumableBatchesByMaterial
## from .views.raw_material_batch import RawMaterialAcceptanceTest
# from .views.consumable_accepatance import ConAcceptanceTestList,ConAcceptanceTestAdd
## from .views.raw_test import RawMaterialAcceptanceTestAdd
from .views.consumable_batch import ConsumableBatchAcceptenceTest
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

path('consumable-list/', ConsumableListFetchView.as_view(), name='consumable-list'),
path('consumable-add/', ConsumableAdd.as_view(), name='consumable-add'),
path('consumable-list/<int:batch_id>/', ConsumableListFetchView.as_view(), name='consumable-update'),
path('update-consumable-status/<str:consumableId>/', UpdateConsumableStatusView.as_view(), name='update-consumable-status'),
path('consumable-list/delete/<int:consumableId>/',DeleteConsumableView.as_view(), name='consumable-delete'),
path('consumable-document/add/',AddConsumableDocumentView.as_view(), name='add-consumable-document'),
path('view-consumable/<int:consumableId>/', ViewConsumableDetailView.as_view(), name='view-consumable'),

path('consumable-batches/<int:material_id>/', ConsumableBatchesByMaterial.as_view(), name='consumable-batches'),

# Rawmaterial_detailed_view
path('consumable-detiled-view/', ConsumableDetailView.as_view(), name='consumable-detiled-view'),
# Rawmaterial_detailed_view
path('consumable-detiled-view/<int:batch_id>/',ConsumableDetailView.as_view(), name='consumable-detiled-view-new'),
# path('rawmaterial-acceptance-add/',RawMaterialAcceptanceTestAdd.as_view(),name='raw-material-acceptance-add'),




path('consumable-batch-fetch/', ConsumableBatchFetchView.as_view(), name='consumable-batch-fetch'),
path('consumable-batch-fetch/<int:batch_id>/', ConsumableBatchFetchView.as_view(), name='consumable-batch-fetch-detail'),
path('consumable-batch-fetch/edit/<int:batch_id>/', ConsumableBatchEditView.as_view(), name='consumable-batch-edit'),

path('consumable-add-batch/', ConsumableBatchAddView.as_view(), name='consumable-batch-add'),
path('consumable-batch-test-add/',ConsumableBatchAcceptenceTest.as_view(),name='consumable-batch-test-add'),
path('view/consumable-batch/<path:batchId>/', ViewConsumableBatchDetailView.as_view(), name='view-consumable-batch'),

path('conbatch-list/delete/<path:conbatchId>/', DeleteConsumableBatchView.as_view(), name='conbatch-delete'),
# path('con-acceptance-add/',ConAcceptanceTestAdd.as_view(),name='con-acceptance-add'),
# path('con-acceptance-list/',ConAcceptanceTestList.as_view(),name='con-acceptance-list'),



# BATCH LIST DETAILED VIEW

path('batch/<str:batch_id>/', ConsumableBatchDetailView.as_view(), name='batch_detail'),

path('consumable-id/<int:material_id>/', ConsumableByid.as_view(), name='consumable-id'),








]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


