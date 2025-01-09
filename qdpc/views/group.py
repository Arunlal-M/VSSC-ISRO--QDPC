from rest_framework.views import APIView  # Import APIView from Django REST framework
from rest_framework.response import Response  # Import Response to send HTTP responses
from django.contrib.auth.models import Group, Permission  # Import Group and Permission models
from rest_framework.permissions import IsAuthenticated  # Import permission class to ensure user is authenticated
from rest_framework import status  # Import status to handle HTTP status codes
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

class GroupListView(APIView):  # Create a class for the API view to list all groups
    permission_classes = [IsAuthenticated]  # Set permission to allow only authenticated users

    def get(self, request):  # Define the GET method for retrieving groups
        groups = Group.objects.all()  # Query all groups from the database
        group_list = [{"id": group.id, "name": group.name} for group in groups]  # Create a list of dictionaries with group ID and name
        
        context = {
            'groups' : groups,
            'group_list': group_list,
        }
        return render(request, 'group_list.html', context)
    
    @csrf_exempt
    def post(self, request):
        group_name = request.data.get('group_name')
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                return Response({'message': 'Group created successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Group already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Group name is required.'}, status=status.HTTP_400_BAD_REQUEST)