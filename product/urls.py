from django.contrib import admin
from .views.raw_material import AddRawMaterialDocumentView, RawMaterialAdd,RawMatrialListFetchView,UpdateRawmaterialStatusView,DeleteRawMatrialView,ViewRawMaterialDetailView#,RawmatrialDetailView
from .views.raw_material_batch import RawMaterialBatchDetailView, RawMatrialBatchFetchView,RawMatrialBatchAddView,RawMatrialBatchEditView,DeleteRawMatrialBatchView,ViewRawMaterialBatchDetailView,RawMaterialBatchesByMaterial
# from .views.raw_material_batch import RawMaterialAcceptanceTest
from .views.product_view import ProductListView
from .views.raw_matrial_accepatance import AcceptanceTestAdd,AcceptanceTestList,DeleteAcceptanceView,ViewAcceptanceTestDetailView
# from .views.raw_test import RawMaterialAcceptanceTestAdd
from .views.raw_material_batch import RawmatrialBatchAcceptenceTest
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .views.product_view import ProductListView,ProductAddView,DeleteProductView,UpdateProductStatusView,AddProductDocumentView,ViewProductDetailView,ProductUpdateView
from .views.ProductBatch import *
from product.views.product import *  
from .views.ProductBatch_clean import ProductBatchApproveView, ProductBatchQAApprovalView, SubmitToSectionView, SubmitToDivisionView, RejectBatchView, ProductBatchQARReportView

raw_material_batch_add_view = RawMatrialBatchAddView()

urlpatterns = [

    path('', product_home, name='product-home'), 

path('raw-material/', RawMatrialListFetchView.as_view(), name='raw-material'),
path('raw-material-add/', RawMaterialAdd.as_view(), name='raw-material-add'),
path('raw-material/<int:batch_id>/', RawMatrialListFetchView.as_view(), name='raw-material-update'),
path('update-rawmaterial-status/<str:rawId>/', UpdateRawmaterialStatusView.as_view(), name='update-product-status'),
path('raw-material/delete/<int:rawId>/', DeleteRawMatrialView.as_view(), name='raw-material-delete'),
path('raw-material-document/add/', AddRawMaterialDocumentView.as_view(), name='add-raw-material-document'),
path('view/raw-material/<int:rawId>/', ViewRawMaterialDetailView.as_view(), name='view-raw-material'),

path('product-batch/<int:batch_id>/', ProductBatchDetailView.as_view(), name='product-batch-detail'),


# Rawmaterial_detailed_view
# path('rawmaterial-detiled-view/', RawmatrialDetailView.as_view(), name='rawmaterial-detiled-view'),
# Rawmaterial_detailed_view
# path('rawmaterial-detiled-view/<int:batch_id>/', RawmatrialDetailView.as_view(), name='rawmaterial-detiled-view-new'),
# path('rawmaterial-acceptance-add/',RawMaterialAcceptanceTestAdd.as_view(),name='raw-material-acceptance-add'),

path('list-view/', ProductListView.as_view(), name='product-list-create'),


path('rawmaterial-batch-fetch/', RawMatrialBatchFetchView.as_view(), name='raw-material-batch-fetch'),
path('rawmaterial-batch-fetch/<int:batch_id>/', RawMatrialBatchFetchView.as_view(), name='raw-material-batch-fetch-detail'),
path('rawmaterial-batch-fetch/edit/<path:batch_id>/', RawMatrialBatchEditView.as_view(), name='raw-material-batch-edit'),
path('raw-material-batches/<int:material_id>/', RawMaterialBatchesByMaterial.as_view(), name='raw-material-batches'),

path('rawmaterial-add-batch/', RawMatrialBatchAddView.as_view(), name='raw-material-batch-add'),
# path('get-acceptance-tests/', raw_material_batch_add_view.get_acceptance_tests, name='get-acceptance-tests'),
# path('rawmaterial-batch-test-add/',RawmatrialBatchAcceptenceTest.as_view(),name='rawmaterial-batch-test-add'),

path('rawmaterial-batch-fetch/', RawMatrialBatchAddView.as_view(), name='raw-material-batch-fetch'),
path('rawmaterial-batch-test-add/', RawmatrialBatchAcceptenceTest.as_view(), name='rawmaterial-batch-test-add'),
path('rawbatch-list/delete/<path:rawbatchId>/', DeleteRawMatrialBatchView.as_view(), name='rawbatch-delete'),
path('view/raw-material-batch/<path:batchId>/', ViewRawMaterialBatchDetailView.as_view(), name='view-raw-material-batch'),



path('acceptance-add/',AcceptanceTestAdd.as_view(),name='acceptance-add'),
path('acceptance-list/',AcceptanceTestList.as_view(),name='acceptance-list'),
path('acceptancetest-list/delete/<path:acceptancetestId>/', DeleteAcceptanceView.as_view(), name='acceptance-delete'),
path('view/acceptancetest/<int:acceptanceTestId>/', ViewAcceptanceTestDetailView.as_view(), name='view-acceptancetest'),



path('list-view/',ProductListView.as_view(),name='product-view'),
path('product-add/',ProductAddView.as_view(),name='product-add'),
path('list-view/<int:productId>/',DeleteProductView.as_view(),name='product-delete'),
path('update-product-status/<int:productId>/', UpdateProductStatusView.as_view(), name='update-product-status'),
path('product/<int:productId>/edit/', ProductUpdateView.as_view(), name='product-edit'),
path('product-document/add/', AddProductDocumentView.as_view(), name='add-product-document'),
path('view-product/<int:productId>/', ViewProductDetailView.as_view(), name='view-product-detail'),

#product batch
path('product-batches/',ProductBatchFetchView.as_view(), name='product-batch-list'),
path('product-batches/add/',ProductBatchAddView.as_view(), name='product-batch-add'),
path('product-batches/<int:pk>/edit/', ProductBatchEditView.as_view(), name='product-batch-edit'),
path('product-batches/<int:pk>/approve/', ProductBatchApproveView.as_view(), name='product-batch-approve'),
path('product-batches/<int:pk>/reject/', ProductBatchRejectView.as_view(), name='product-batch-reject'),
path('api/raw-materials/', RawMaterialBatchListView.as_view(), name='raw-materials-api'),
path('api/components/', ComponentBatchListView.as_view(), name='component-api'),
path('api/consumables/', ConsumableWithBatchesAPIView.as_view(), name='consumables-with-batches'),
path('api/drawings/', DrawingListByProductAPIView.as_view(), name='drawings-by-product'),
path('api/get-rawacceptance-tests/', RawMaterialAcceptanceTestListAPIView.as_view(), name='get-raw-acceptance-tests'),
path('api/get-process/', RawMaterialProcessListAPIView.as_view(), name='get-acceptance-tests'),
path('api/get-equpment/', ProductEquipmentsApiView.as_view(), name='get-equpment'),
path('api/get-acceptance-tests/', ProductAcceptanceTestApiView.as_view(), name='get-acceptance-tests'),


 path('product-batch/<int:pk>/report/', SingleProductBatchReportView.as_view(), name='product-batch-single-report'),
    
    path('product-batch/<int:pk>/delete/', ProductBatchDeleteView.as_view(), name='product-batch-delete'),

path('product-batch/view/<int:pk>/', SingleProductBatchView.as_view(), name='product-batch-single-view'),
path('product-batches/<int:pk>/', SingleProductBatchView.as_view(), name='product-batch-view'),

# Product batch approval endpoint
path('product-batch/<int:batch_id>/approve/', ProductBatchApproveView.as_view(), name='product-batch-approve'),

# Product batch QA approval page
path('product-batch/<int:batch_id>/qa-approval/', ProductBatchQAApprovalView.as_view(), name='product-batch-qa-approval'),

# Product batch QAR report download
path('product-batch/<int:batch_id>/qar-report/', ProductBatchQARReportView.as_view(), name='product-batch-qar-report'),

# Hierarchical approval workflow endpoints
path('product-batch/<int:batch_id>/submit-to-section/', SubmitToSectionView.as_view(), name='submit-to-section'),
path('product-batch/<int:batch_id>/submit-to-division/', SubmitToDivisionView.as_view(), name='submit-to-division'),
path('product-batch/<int:batch_id>/reject/', RejectBatchView.as_view(), name='reject-batch'),

# BATCH LIST DETAILED VIEW

path('batch/<str:batch_id>/', RawMaterialBatchDetailView.as_view(), name='batch_detail'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

