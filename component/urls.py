from django.contrib import admin
from .views.component import ComponentAdd
from.views.component import ComponentListFetchView,ComponentDetailView,DeleteComponentView,UpdateComponentStatusView
from .views.component_batch import ComponentBatchFetchView,ComponentBatchAddView
from .views.component_batch import ComponentBatchAcceptenceTest
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

path('component-list/', ComponentListFetchView.as_view(), name='component-list'),
path('component-add/', ComponentAdd.as_view(), name='component-add'),
path('component-list/<int:batch_id>/', ComponentListFetchView.as_view(), name='component-update'),
path('update-component-status/<str:componentId>/', UpdateComponentStatusView.as_view(), name='update-component-status'),
path('component-list/delete/<int:componentId>/',DeleteComponentView.as_view(), name='component-delete'),




# Rawmaterial_detailed_view
path('component-detailed-view/', ComponentDetailView.as_view(), name='component-detailed-view'),
# Rawmaterial_detailed_view
path('component-detailed-view/<int:batch_id>/',ComponentDetailView.as_view(), name='component-detailed-view-new'),
# path('rawmaterial-acceptance-add/',RawMaterialAcceptanceTestAdd.as_view(),name='raw-material-acceptance-add'),




path('component-batch-fetch/', ComponentBatchFetchView.as_view(), name='component-batch-fetch'),
path('component-batch-fetch/<int:batch_id>/', ComponentBatchFetchView.as_view(), name='component-batch-fetch-detail'),
path('component-add-batch/', ComponentBatchAddView.as_view(), name='component-batch-add'),
path('component-batch-test-add/',ComponentBatchAcceptenceTest.as_view(),name='component-batch-test-add'),










]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


