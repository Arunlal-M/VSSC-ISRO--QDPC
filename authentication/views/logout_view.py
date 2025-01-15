# from rest_framework.views import APIView
# from qdpc.core.modelviewset import BaseModelViewSet
# from rest_framework import status
# from rest_framework.response import Response
# from qdpc.core import constants
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from authentication.serializers.login_serializer import LoginSerializer
# from qdpc.services.login_service import LoginService
# from django.shortcuts import render, redirect

# from qdpc_core_models.models.user import User

# class Logout(APIView):
#     """
#     Logout API: Logs out the user by deleting their authentication token.
#     """
#     permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

#     def post(self, request):
#         user = request.user
#         success, message = LogoutService.logout_user(user)
        
#         if success:
#             return Response({
#                 'success': True,
#                 'message': message
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#                 'success': False,
#                 'message': message
#             }, status=status.HTTP_400_BAD_REQUEST)



# File: views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout

class LogoutAPIView(APIView):
    """
    Handles user logout for authenticated users.
    Requires authentication and logs the user out.
    """
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this

    def post(self, request, *args, **kwargs):
        
        print("Logout api is hit")
        # Perform the logout
        logout(request)

        # Return a success response
        return Response({"message": "Successfully logged out."}, status=200)
