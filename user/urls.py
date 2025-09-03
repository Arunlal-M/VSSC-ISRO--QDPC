from django.contrib import admin
from django.urls import path,include
from .views.user_dashbord import UserDashboard
from .views.userlist_view import UserFetch,UserListView,UserProfileView
from .views.user_edit_page import UserEditPageView
from .views.user_approval import UserApprovalView,UpdateUserStatusView,RejectUserView
urlpatterns = [
    path('user-dashboard/', UserDashboard.as_view(), name='user-dashboard'),
    path('user-fetch/', UserFetch.as_view(), name='user-fetch'),
    path('userlist/', UserListView.as_view(), name='user-list'),
    path('user-update/<int:user_id>/', UserListView.as_view(), name='user-update'),
    path('user-edit/<int:user_id>/', UserEditPageView.as_view(), name='user-edit-page'),
    path('approve-user/<int:user_id>/', UserApprovalView.as_view(), name='approve-user'),
    path('api/update-user-status/', UpdateUserStatusView.as_view(), name='update_user_status'),
    path('reject-user/<int:user_id>/', RejectUserView.as_view(), name='reject-user'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),

]