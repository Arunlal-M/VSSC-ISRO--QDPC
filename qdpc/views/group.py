from rest_framework.views import APIView  # Import APIView from Django REST framework
from rest_framework.response import Response  # Import Response to send HTTP responses
from django.contrib.auth.models import Group, Permission  # Import Group and Permission models
from rest_framework.permissions import IsAuthenticated  # Import permission class to ensure user is authenticated
from rest_framework import status  # Import status to handle HTTP status codes
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect  # Import render and redirect for template rendering and redirection
from qdpc.core.decorators import require_admin_permission


class GroupListView(APIView):  # Create a class for the API view to list all groups
    permission_classes = [IsAuthenticated]  # Set permission to allow only authenticated users

    def get(self, request):  # Define the GET method for retrieving groups
        # Check if user has admin permissions using dynamic permission system
        from qdpc.core.permissions import has_page_permission
        if not (request.user.is_superuser or has_page_permission(request.user, 'Groups', 'view')):
            return redirect('user-dashboard')
        # Simple search by name
        query_text = (request.GET.get('q') or '').strip()
        groups = Group.objects.all()
        if query_text:
            groups = groups.filter(name__icontains=query_text)
        group_list = [{"id": group.id, "name": group.name} for group in groups]
        
        context = {
            'groups': groups,
            'group_list': group_list,
            'q': query_text,
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