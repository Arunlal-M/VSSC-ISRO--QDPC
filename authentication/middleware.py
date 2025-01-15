from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse

class RedirectUnauthorizedMiddleware:
    """
    Middleware to redirect unauthorized requests to the login page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Middleware: Checking request authentication")

        # Check if the user is not authenticated
        if not request.user.is_authenticated:
            print("User is not authenticated")

            # Exclude specific endpoints (e.g., login URL)
            excluded_paths = [reverse('login_view'), reverse('logout_view')]
            if request.path not in excluded_paths:
                
                # For API requests (JSON content)
                if request.path.startswith('/api/') or request.content_type == 'application/json':
                    return JsonResponse({'detail': 'Unauthorized. Redirecting to login.'}, status=401)

                # Redirect to login page for non-API requests
                return redirect(reverse('login_view'))

        # If authenticated, allow the request to proceed
        return self.get_response(request)
