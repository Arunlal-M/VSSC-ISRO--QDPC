from django.contrib import admin
from django.urls import path,include
from .views.source import SourceListView,DeleteSourceView
from .views.supplier import SupplierListView,DeleteSupplierView
from .views.division import DivisionListView,DeleteDivisonView
from .views.center import CenterListView,DeleteCenterView
from .views.unit import UnitView,DeleteUnitView
from .views.group import GroupListView
from .views.permission import GroupPermissionListView  # Import the views from the views module
from .views.grade import GradeView,DeleteGradeView
from .views.enduse import EnduseView,DeleteEnduseView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('authentication.urls')),
    path('user/',include('user.urls')),
    path('product/',include('product.urls')),
    path('equipment/',include('equipment.urls')),
    path('process/',include('process.urls')),
    path('consumable/',include('consumable.urls')),
    path('component/',include('component.urls')),

    path('sources/', SourceListView.as_view(), name='source-list'),
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),
    path('centers/', CenterListView.as_view(), name='center-list'),
    path('centers/<int:centerId>/', DeleteCenterView.as_view(), name='center-delete'),
    
    path('divisions/', DivisionListView.as_view(), name='division-list'),
    path('divisions/<int:divisionId>/', DeleteDivisonView.as_view(), name='division-delete'),
    
    path('divisions/center/<int:center_id>/', DivisionListView.as_view(), name='get-divisions-by-center'),    
    path('sources/<int:sourceId>/', DeleteSourceView.as_view(), name='source-delete'),
    path('suppliers/<int:supplierId>/', DeleteSupplierView.as_view(), name='delete-supplier'),
   
    path('unit/', UnitView.as_view(), name='unit-list'),
    path('unit/<int:unitId>/', DeleteUnitView.as_view(), name='delete-unit'),
    
    
    
    path('grade/', GradeView.as_view(), name='grade-list'),
    path('grade/<int:gradeId>/', DeleteGradeView.as_view(), name='delete-grade'),
    
    path('enduse/', EnduseView.as_view(), name='enduse-list'),
    path('enduse/<int:enduseId>/', DeleteEnduseView.as_view(), name='enduse-grade'),
    
    path('groups/', GroupListView.as_view(), name='group-list'),  # Map the URL to the GroupListView

    path('groups/<int:group_id>/permissions/', GroupPermissionListView.as_view(), name='group-permission-list'),  # Map the URL to the GroupPermissionListView
    path('groups/create/', GroupListView.as_view(), name='group-create'),
    path('groups/<int:group_id>/delete/', GroupPermissionListView.as_view(), name='group-delete'),  # URL to delete a group
]


