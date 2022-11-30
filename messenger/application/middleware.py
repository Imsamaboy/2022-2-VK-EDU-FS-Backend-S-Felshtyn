from django.conf import settings
from django.contrib.auth.views import redirect_to_login

IGNORE_URLS = []
if hasattr(settings, "LOGIN_IGNORE_URLS"):
    IGNORE_URLS += settings.LOGIN_IGNORE_URLS


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def is_ignored_path(self, path):
        for ignore_path in IGNORE_URLS:
            if path.startswith(ignore_path):
                return True
        return False

    def process_view(self, request, view_func, view_args, view_kwargs):
        if self.is_ignored_path(request.path):
            return None
        if not request.user.is_authenticated:
            return redirect_to_login(next=request.path)
