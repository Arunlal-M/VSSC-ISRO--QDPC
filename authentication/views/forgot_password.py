
from qdpc.core import constants
from rest_framework import status
from qdpc.services.login_service import LoginService
from qdpc.core.modelviewset import BaseModelViewSet
from django.shortcuts import render, redirect
from authentication.serializers.password_reset_serailizer import ResetPasswordSerializer

class ForgotPasswordAPIView(BaseModelViewSet):

    def get(self,request):

        return render(request,'forgot_password_two.html')

    def post(self,request):

        serializer = ResetPasswordSerializer(data=request.data)
        success = False
        message = constants.RESET_EMAIL_FAILED
        status_code = status.HTTP_400_BAD_REQUEST
        data = request.data

        try:
            if serializer.is_valid():
                email = serializer.validated_data['email']
                message, success, status_code = LoginService.reset_password_request(email)   
            exception_message = None
        except Exception as ex:
            success = False
            message = constants.RESET_EMAIL_FAILED
            status_code = status.HTTP_400_BAD_REQUEST
        return self.render_response(data, success, message, status_code)




