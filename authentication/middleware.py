from django.shortcuts import redirect
from django.urls import reverse, resolve
from django.http import JsonResponse
import threading

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

class ThreadLocalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.user = getattr(request, 'user', None)
        response = self.get_response(request)
        return response

class RedirectUnauthorizedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            view_name = resolve(request.path_info).view_name
        except Exception:
            view_name = None

        excluded_view_names = [
            'login_view',
            'logout_view',
            'sign-up',
            'forgot_username',
            'forgot_password',
        ]

        # If the path is in excluded list, skip auth check
        if view_name in excluded_view_names:
            return self.get_response(request)

        # If user is not authenticated
        if not request.user.is_authenticated:
            if request.path.startswith('/api/') or request.content_type == 'application/json':
                return JsonResponse({'detail': 'Unauthorized. Redirecting to login.'}, status=401)
            return redirect(reverse('login_view'))

        return self.get_response(request)
