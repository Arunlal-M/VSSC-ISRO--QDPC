
from qdpc.core.modelviewset import BaseModelViewSet,BaseViewSet
from rest_framework import status
from rest_framework.response import Response
from qdpc.core import constants
from rest_framework.permissions import IsAuthenticated, AllowAny
from authentication.serializers.login_serializer import LoginSerializer
from qdpc.services.login_service import LoginService
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

class UserDashboard(BaseViewSet):
    """User Dashborad for the logged in user"""
    # authentication_classes = [TokenAuthentication]
    

    def get(self, request):

        name = request.GET.get('name', 'User')  # Retrieve the name from the session, default to 'User' if not found
        return render(request, 'dashboardtwo.html', {"name": name})

    