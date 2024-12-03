from django.contrib import admin
from django.urls import path,include
from .views.login_view import Login
from .views.signup_view import Signup
from .views.forgot_username import ForgotUsername
from .views.forgot_password import ForgotPasswordAPIView
from .views.reset_password import PasswordResetUpdateAPIView
urlpatterns = [
   
    path('',Login.as_view(), name='default_view'),
    path('login/',Login.as_view(), name='login_view'),
    path('sign-up/',Signup.as_view(),name='sign-up'),
    # path('get-divisions/<int:center_id>/', Signup.get_divisions, name='get-divisions'),
    path('get_centers/', Signup.get_centers, name='get_centers'),
    path('forgot-username/',ForgotUsername.as_view(),name='forgot-username'),
    path('forgot-password/',ForgotPasswordAPIView.as_view(),name='forgot-password'),
    path('reset-password/',PasswordResetUpdateAPIView.as_view(),name='reset-password')

    
]
