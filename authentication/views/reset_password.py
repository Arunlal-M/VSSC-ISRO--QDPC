from qdpc.core import constants
from rest_framework import status
from qdpc.services.login_service import LoginService
from authentication.serializers.forgot_username_serializer import ForgotUsernameSerializer
from qdpc.core.modelviewset import BaseModelViewSet
from django.shortcuts import render, redirect
from authentication.serializers.password_reset_serailizer import ResetPasswordSerializer,UpdatePasswordSerializer





class PasswordResetUpdateAPIView(BaseModelViewSet):

    def get(self,request):

        return render(request,'reset_pasword_two.html')
    
    def post(self, request, format=None):
        print("Entered put")
        data = {}
        print(request.data)
        success = False
        status_code = status.HTTP_400_BAD_REQUEST
        message = constants.RESET_EMAIL_FAILED
       
        serializer = UpdatePasswordSerializer(data=request.data)
        try:
            if serializer.is_valid():
                print("is vlaid")
                reset_key = serializer.validated_data['reset_key']
                password = serializer.validated_data['password']
                message, success, status_code = LoginService.update_password_request(reset_key, password)   
            exception_message = None         
        except Exception as ex:
            success = False
            message = constants.RESET_EMAIL_FAILED
            status_code = status.HTTP_400_BAD_REQUEST
        return self.render_response(data, success, message, status_code)
