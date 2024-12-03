from django.contrib import admin
from .views.raw_material import AddRawMaterialDocumentView, RawMaterialAdd,RawMatrialListFetchView,UpdateRawmaterialStatusView,DeleteRawMatrialView#,RawmatrialDetailView
from .views.raw_material_batch import RawMaterialBatchDetailView, RawMatrialBatchFetchView,RawMatrialBatchAddView
# from .views.raw_material_batch import RawMaterialAcceptanceTest
from .views.product_view import ProductListView
from .views.raw_matrial_accepatance import AcceptanceTestAdd,AcceptanceTestList
# from .views.raw_test import RawMaterialAcceptanceTestAdd
from .views.raw_material_batch import RawmatrialBatchAcceptenceTest
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .views.product_view import ProductListView,ProductAddView,DeleteProductView,UpdateProductStatusView


urlpatterns = [

path('raw-material/', RawMatrialListFetchView.as_view(), name='raw-material'),
path('raw-material-add/', RawMaterialAdd.as_view(), name='raw-material-add'),
path('raw-material/<int:batch_id>/', RawMatrialListFetchView.as_view(), name='raw-material-update'),
path('update-rawmaterial-status/<str:rawId>/', UpdateRawmaterialStatusView.as_view(), name='update-product-status'),
path('raw-material/delete/<int:rawId>/', DeleteRawMatrialView.as_view(), name='raw-material-delete'),
path('raw-material-document/add/', AddRawMaterialDocumentView.as_view(), name='add-raw-material-document'),



# Rawmaterial_detailed_view
# path('rawmaterial-detiled-view/', RawmatrialDetailView.as_view(), name='rawmaterial-detiled-view'),
# Rawmaterial_detailed_view
# path('rawmaterial-detiled-view/<int:batch_id>/', RawmatrialDetailView.as_view(), name='rawmaterial-detiled-view-new'),
# path('rawmaterial-acceptance-add/',RawMaterialAcceptanceTestAdd.as_view(),name='raw-material-acceptance-add'),

path('list-view/', ProductListView.as_view(), name='product-list-create'),


path('rawmaterial-batch-fetch/', RawMatrialBatchFetchView.as_view(), name='raw-material-batch-fetch'),
path('rawmaterial-batch-fetch/<int:batch_id>/', RawMatrialBatchFetchView.as_view(), name='raw-material-batch-fetch-detail'),

path('rawmaterial-add-batch/', RawMatrialBatchAddView.as_view(), name='raw-material-batch-add'),
# path('rawmaterial-batch-test-add/',RawmatrialBatchAcceptenceTest.as_view(),name='rawmaterial-batch-test-add'),

path('rawmaterial-batch-fetch/', RawMatrialBatchAddView.as_view(), name='raw-material-batch-fetch'),
path('rawmaterial-batch-test-add/', RawmatrialBatchAcceptenceTest.as_view(), name='rawmaterial-batch-test-add'),


path('acceptance-add/',AcceptanceTestAdd.as_view(),name='acceptance-add'),
path('acceptance-list/',AcceptanceTestList.as_view(),name='acceptance-list'),



path('list-view/',ProductListView.as_view(),name='product-view'),
path('product-add/',ProductAddView.as_view(),name='product-add'),
path('list-view/<str:productId>/',DeleteProductView.as_view(),name='product-delete'),
path('update-product-status/<str:productId>/', UpdateProductStatusView.as_view(), name='update-product-status'),

# BATCH LIST DETAILED VIEW

path('batch/<str:batch_id>/', RawMaterialBatchDetailView.as_view(), name='batch_detail'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


