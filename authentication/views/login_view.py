from rest_framework.views import APIView
from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework import status
from rest_framework.response import Response
from qdpc.core import constants
from rest_framework.permissions import IsAuthenticated, AllowAny
from authentication.serializers.login_serializer import LoginSerializer
from qdpc.services.login_service import LoginService
from django.shortcuts import render, redirect

from qdpc_core_models.models.user import User
class Login(BaseModelViewSet):
    """ Login Api for qdpc application"""

    def get(self,request):
        return render(request,'logintwo.html')

    def post(self, request):
        data={}
        success=False
        message=constants.USERNAME_PASSWORD_EMPTY
        status_code=status.HTTP_403_FORBIDDEN
        serializer = LoginSerializer(data=request.data)
        try:
            if serializer.is_valid():
                username = serializer.validated_data.get('username')
                password = serializer.validated_data.get('password')
                success, status_code, data, message = LoginService.login_username(username=username,password=password)
            else:
                pass
        
        except Exception as ex:
            success = False
            message = constants.USERNAME_PASSWORD_EMPTY
            status_code = status.HTTP_400_BAD_REQUEST
            
        return self.render_response(data,success, message, status_code)

