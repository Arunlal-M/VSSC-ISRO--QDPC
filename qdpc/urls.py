from django.contrib import admin
from django.urls import path,include
from .views.source import SourceListView,DeleteSourceView,EditSourceView
from .views.supplier import SupplierListView,DeleteSupplierView,EditSupplierView
from .views.division import DivisionListView,DeleteDivisonView,EditDivisionView,DivisionAjax
from .views.center import CenterListView,DeleteCenterView,EditCenterView
from .views.unit import UnitView,DeleteUnitView,EditUnitView
from .views.group import GroupListView
from .views.permission import GroupPermissionListView  # Import the views from the views module
from .views.grade import GradeView,DeleteGradeView,EditGradeView
from .views.enduse import EnduseView,DeleteEnduseView,EditEnduseView
from .views.product_category import ProductCategoryView,DeleteProductCategoryView,EditProductCategoryView
from .views.document_type import DocumentTypeView,DeleteDocumentTypeView,EditDocumentTypeView
from .views.notification import view_all_notifications,mark_notification_as_read
from .views.dashboard import DashboardSummaryAPI,ResourceStatusAPI,InventoryTrendsAPI,InventoryDistributionAPI,RecentActivityAPI
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('authentication.urls')),
    path('user/',include('user.urls')),
    path('product/',include('product.urls')),
    path('api/dashboard/summary/', DashboardSummaryAPI.as_view(), name='dashboard-summary'),
    path('api/dashboard/status/', ResourceStatusAPI.as_view(), name='resource-status'),
    path('api/dashboard/trends/', InventoryTrendsAPI.as_view(), name='inventory-trends'),
    path('api/dashboard/activity/', RecentActivityAPI.as_view(), name='recent-activity'),


    path('api/dashboard/distribution/', InventoryDistributionAPI.as_view(), name='inventory-distribution'),
    path('equipment/',include('equipment.urls')),
    path('process/',include('process.urls')),
    path('consumable/',include('consumable.urls')),
    path('component/',include('component.urls')),
    path('report/',include('report.urls')),
    path('stage-clearance/',include('stage_clearance.urls')),
    path('notifications/', view_all_notifications, name='view_all_notifications'),
    path('notifications/mark_as_read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),

    path('sources/', SourceListView.as_view(), name='source-list'),
    path('sources/view/<int:sourceId>/', EditSourceView.as_view(), name='source-view'),
    path('sources/edit/<int:sourceId>/', EditSourceView.as_view(), name='source-edit'),
    path('suppliers/view/<int:supplierId>/', EditSupplierView.as_view(), name='supplier-view'),
    path('suppliers/edit/<int:supplierId>/', EditSupplierView.as_view(), name='supplier-edit'),
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),
    # path('suppliers/edit/<int:supplierId>/', SupplierListView.as_view(), name='supplier-list'),
    
    
    path('centers/', CenterListView.as_view(), name='center-list'),
    path('centers/view/<int:centerId>/', EditCenterView.as_view(), name='center-view'),
    path('centers/edit/<int:centerId>/', EditCenterView.as_view(), name='center-edit'),
    path('centers/<int:centerId>/', DeleteCenterView.as_view(), name='center-delete'),
    
    path('divisions/', DivisionListView.as_view(), name='division-list'),
    path('divisions/view/<int:divisionId>/', EditDivisionView.as_view(), name='division-view'),
    path('divisions/edit/<int:divisionId>/', EditDivisionView.as_view(), name='division-edit'),
    path('divisions/<int:divisionId>/', DeleteDivisonView.as_view(), name='division-delete'),
    
    path('divisions/center/<int:center_id>/', DivisionAjax.as_view(), name='get-divisions-by-center'),    
    path('sources/<int:sourceId>/', DeleteSourceView.as_view(), name='source-delete'),
    path('suppliers/<int:supplierId>/', DeleteSupplierView.as_view(), name='delete-supplier'),
   
    path('unit/', UnitView.as_view(), name='unit-list'),
    path('unit/<int:unitId>/', DeleteUnitView.as_view(), name='delete-unit'),
    path('unit/view/<int:unitId>/', EditUnitView.as_view(), name='unit-view'),
    path('unit/edit/<int:unitId>/', EditUnitView.as_view(), name='unit-edit'),
    
    
    
    path('grade/', GradeView.as_view(), name='grade-list'),
    path('grade/<int:gradeId>/', DeleteGradeView.as_view(), name='delete-grade'),
    path('grade/view/<int:gradeId>/', EditGradeView.as_view(), name='grade-view'),
    path('grade/edit/<int:gradeId>/', EditGradeView.as_view(), name='grade-edit'),
    
    
    path('enduse/', EnduseView.as_view(), name='enduse-list'),
    path('enduse/<int:enduseId>/', DeleteEnduseView.as_view(), name='enduse-grade'),
    path('enduse/view/<int:enduseId>/', EditEnduseView.as_view(), name='enduse-view'),
    path('enduse/edit/<int:enduseId>/', EditEnduseView.as_view(), name='enduse-edit'),
    
    path('productcategory/', ProductCategoryView.as_view(), name='productcategory-list'),
    path('productcategory/<int:productcategoryId>/', DeleteProductCategoryView.as_view(), name='delete-productcategory'),
    path('productcategory/view/<int:productcategoryId>/', EditProductCategoryView.as_view(), name='productcategory-view'),
    path('productcategory/edit/<int:productcategoryId>/', EditProductCategoryView.as_view(), name='productcategory-edit'),
    
    
    path('documenttype/', DocumentTypeView.as_view(), name='documenttype-list'),
    path('documenttype/<int:documenttypeId>/', DeleteDocumentTypeView.as_view(), name='delete-documenttype'),
    path('documenttype/view/<int:documenttypeId>/', EditDocumentTypeView.as_view(), name='documenttype-view'),
    path('documenttype/edit/<int:documenttypeId>/', EditDocumentTypeView.as_view(), name='documenttype-edit'),
    
    
    path('groups/', GroupListView.as_view(), name='group-list'),  # Map the URL to the GroupListView

    path('groups/<int:group_id>/permissions/', GroupPermissionListView.as_view(), name='group-permission-list'),  # Map the URL to the GroupPermissionListView
    path('groups/create/', GroupListView.as_view(), name='group-create'),
    path('groups/<int:group_id>/delete/', GroupPermissionListView.as_view(), name='group-delete'),  # URL to delete a group
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

