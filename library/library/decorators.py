from django.shortcuts import redirect
from functools import wraps



def role_required(required_role, login_url='login'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role == required_role:
                return view_func(request, *args, **kwargs)
            else:
                return redirect(login_url)
        return _wrapped_view
    return decorator
